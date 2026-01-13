"""PDF export functionality for Jupyter notebooks.

Enhanced PDF export with support for:
- JupyterHub
- Local JupyterLab
- Google Colab
- Notebook attachment to PDF
- Auto-save before export

Adapted from:
- https://forums.fast.ai/t/jupyter-notebook-enhancements-tips-and-tricks/17064/39
- https://discourse.jupyter.org/t/how-to-get-kernel-state-from-running-local-jupyter-notebook/15028/6
"""

import base64
import io
import json
import os
import re
import time
import shlex
from pathlib import Path

import requests
import ipykernel
import nbformat
from jupyter_server import serverapp
from nbconvert import WebPDFExporter
try:
    from nbconvert import PDFExporter
    _LATEX_AVAILABLE = True
except ImportError:
    _LATEX_AVAILABLE = False
from IPython.core.magic import register_line_magic
from IPython.display import HTML, Markdown, Javascript, display

import warnings
warnings.filterwarnings("ignore")

from .config import config

# Try to import pypdf for attachments
try:
    from pypdf import PdfReader, PdfWriter
    _PYPDF_AVAILABLE = True
except ImportError:
    _PYPDF_AVAILABLE = False

def _ensure_chromium():
    """Ensure chromium is installed for PDF export."""
    try:
        ex = WebPDFExporter()
        ex.run_playwright('')
        return True
    except Exception:
        print("Installing chromium for PDF export (one time)...")
        result = os.system('playwright install chromium')
        return result == 0


def _is_colab():
    """Check if running in Google Colab."""
    try:
        import google.colab
        return True
    except ImportError:
        return False


def _save_notebook(verbose=False):
    """
    Save the current notebook before exporting.

    Uses JavaScript to trigger save in both JupyterLab and classic notebook.
    Returns after a brief delay to allow the save to complete.
    """
    if _is_colab():
        # Colab gets live state from API, no need to save
        return

    if verbose:
        print("Saving notebook...")

    # JavaScript that works in both JupyterLab and classic notebook
    # Each attempt is wrapped in its own try/catch to prevent errors from propagating
    save_js = """
    (function() {
        // Try classic Jupyter notebook first
        try {
            if (typeof IPython !== 'undefined' && IPython.notebook &&
                typeof IPython.notebook.save_checkpoint === 'function') {
                IPython.notebook.save_checkpoint();
                return;
            }
        } catch(e) {}

        // Try Jupyter notebook 7+
        try {
            if (typeof Jupyter !== 'undefined' && Jupyter.notebook &&
                typeof Jupyter.notebook.save_checkpoint === 'function') {
                Jupyter.notebook.save_checkpoint();
                return;
            }
        } catch(e) {}

        // Try JupyterLab - check each property individually
        try {
            if (window.jupyterapp && window.jupyterapp.commands &&
                window.jupyterapp.commands.execute) {
                window.jupyterapp.commands.execute('docmanager:save');
                return;
            }
        } catch(e) {}

        try {
            if (window._JUPYTERLAB && window._JUPYTERLAB.commands &&
                window._JUPYTERLAB.commands.execute) {
                window._JUPYTERLAB.commands.execute('docmanager:save');
                return;
            }
        } catch(e) {}

        // Skip the require() approach entirely - it causes errors in many environments
        // The notebook state will be read from disk, which is usually up-to-date
    })();
    """

    display(Javascript(save_js))

    # Give the save operation time to complete
    time.sleep(1.0)


def _attach_notebook_to_pdf(pdf_bytes, notebook_content, notebook_filename):
    """
    Attach the source notebook (.ipynb) to a PDF file.

    Args:
        pdf_bytes: The PDF file content as bytes
        notebook_content: The notebook content (dict or string)
        notebook_filename: Name for the attached file (e.g., "notebook.ipynb")

    Returns:
        bytes: The PDF with the notebook attached, or original if attachment fails
    """
    if not _PYPDF_AVAILABLE:
        return pdf_bytes

    try:
        # Convert notebook to JSON bytes if it's a dict
        if isinstance(notebook_content, dict):
            nb_bytes = json.dumps(notebook_content, indent=2).encode('utf-8')
        elif isinstance(notebook_content, str):
            nb_bytes = notebook_content.encode('utf-8')
        else:
            nb_bytes = notebook_content

        # Read the PDF
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
        pdf_writer = PdfWriter()

        # Copy all pages
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        # Attach the notebook file
        pdf_writer.add_attachment(notebook_filename, nb_bytes)

        # Write to bytes
        output = io.BytesIO()
        pdf_writer.write(output)
        return output.getvalue()

    except Exception as e:
        # If attachment fails, return original PDF
        print(f"Warning: Could not attach notebook: {e}")
        return pdf_bytes


def get_notebook_path():
    """Returns the absolute path of the Notebook or None if it cannot be determined.

    Works in JupyterHub and local Jupyter environments.
    Returns None if path cannot be determined or if in Colab.
    """
    # Colab is handled separately
    if _is_colab():
        return None

    # Method 1: Try IPython's __session__ (available in some environments)
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip and hasattr(ip, 'user_ns') and '__session__' in ip.user_ns:
            return ip.user_ns['__session__']
    except Exception:
        pass

    # Method 2: Try JPY_SESSION_NAME environment variable (JupyterLab 4+)
    if 'JPY_SESSION_NAME' in os.environ:
        session_name = os.environ['JPY_SESSION_NAME']
        # This is usually just the filename, try to find it
        if os.path.isabs(session_name) and os.path.exists(session_name):
            return session_name

    # Method 3: Query the Jupyter server API (JupyterHub)
    try:
        connection_file = os.path.basename(ipykernel.get_connection_file())
        kernel_id = connection_file.split('-', 1)[1].split('.')[0]

        # Build auth headers
        headers = {}
        if 'JUPYTERHUB_API_TOKEN' in os.environ:
            headers['Authorization'] = f'token {os.environ["JUPYTERHUB_API_TOKEN"]}'

        for srv in serverapp.list_running_servers():
            try:
                # Local server token (from server info)
                if not headers and srv.get('token'):
                    headers['Authorization'] = f'token {srv["token"]}'

                # Build URL with token as query param (fallback for some setups)
                url = srv['url'] + 'api/sessions'
                if not headers.get('Authorization') and srv.get('token'):
                    url += f'?token={srv["token"]}'

                result = requests.get(url, headers=headers, timeout=5)

                if result.status_code == 200:
                    sessions = result.json()
                    for sess in sessions:
                        if sess['kernel']['id'] == kernel_id:
                            return os.path.join(srv['root_dir'], sess['path'])

            except Exception:
                continue

    except Exception:
        pass

    return None


def _normalize_cell_sources(nb):
    """
    Normalize cell sources to strings.

    Jupyter notebook format allows cell sources to be either a string
    or a list of strings. nbconvert's highlightmagics preprocessor
    expects strings, so we normalize here.
    """
    for cell in nb.get('cells', []):
        source = cell.get('source', '')
        if isinstance(source, list):
            cell['source'] = ''.join(source)
    return nb


def _fix_local_images(nb, root_dir):
    """
    Convert relative image paths to absolute paths.

    This fixes the issue where local images don't render in PDF
    because nbconvert generates HTML in a temp directory.
    """
    if not root_dir:
        return nb

    # Regex for markdown images with relative paths
    RE_local_images = re.compile(
        r"!\[(.*?)\]\((?!https?://|[A-Z]:\\|/|~/)(.*?)(\s*[\"'].*?[\"'])?\)"
    )

    for cell in nb['cells']:
        if cell['cell_type'] != 'markdown':
            continue

        offset = 0
        for match in RE_local_images.finditer(cell['source']):
            path = match.group(2)
            fullpath = os.path.realpath(os.path.join(root_dir, path))
            fullpath = fullpath.replace(' ', '%20')

            start = match.start(2) + offset
            end = match.end(2) + offset
            cell['source'] = cell['source'][:start] + fullpath + cell['source'][end:]
            offset += len(fullpath) - (match.end(2) - match.start(2))

    return nb


def _get_source_url(notebook_path):
    """
    Try to construct a source URL for the notebook.

    Supports JupyterHub environments with known URL patterns.
    """
    # JupyterHub environment
    if 'JUPYTERHUB_SERVICE_PREFIX' in os.environ:
        prefix = os.environ['JUPYTERHUB_SERVICE_PREFIX']
        home = os.environ.get('HOME', '')

        if notebook_path.startswith(home):
            rel_path = notebook_path[len(home):].lstrip('/')

            # Try to get base URL from config
            base_url = config.jupyterhub.dev_url

            return f"{base_url}{prefix}lab/tree/{rel_path}"

    return None


def _get_colab_notebook():
    """
    Get notebook content and name from Google Colab.

    Returns:
        tuple: (notebook_dict, notebook_name) or (None, None) if not in Colab
    """
    if not _is_colab():
        return None, None

    try:
        from google.colab import _message

        # Get the notebook content directly from Colab
        ipynb = _message.blocking_request('get_ipynb', timeout_sec=30)

        if ipynb and 'ipynb' in ipynb:
            nb_dict = ipynb['ipynb']

            # Try to get notebook name from metadata or use default
            nb_name = 'notebook'
            if 'metadata' in nb_dict:
                # Colab sometimes stores name in metadata
                nb_name = nb_dict['metadata'].get('colab', {}).get('name', nb_name)
                # Remove .ipynb extension if present
                if nb_name.endswith('.ipynb'):
                    nb_name = nb_name[:-6]

            return nb_dict, nb_name

    except Exception as e:
        error_msg = str(e)
        if 'credential propagation' in error_msg.lower():
            print("Error: Colab credential propagation failed.")
            print("This is usually a temporary issue. Try:")
            print("  1. Save the notebook to Drive (Ctrl+S)")
            print("  2. Refresh the page and re-run")
            print("  3. Reconnect to the runtime (Runtime > Reconnect)")
        elif 'File not found' in error_msg or 'HttpError 404' in error_msg:
            print("Error: Could not retrieve notebook content.")
            print("This often happens when the notebook was opened from GitHub.")
            print("To fix: File > Save a copy in Drive, then run %pdf from that copy.")
        else:
            print(f"Warning: Could not get notebook from Colab: {e}")

    return None, None


def _colab_download(pdf_bytes, filename):
    """Trigger file download in Google Colab."""
    try:
        from google.colab import files

        # Write to temp file and download
        temp_path = f'/tmp/{filename}'
        with open(temp_path, 'wb') as f:
            f.write(pdf_bytes)

        files.download(temp_path)
        return True

    except Exception as e:
        print(f"Warning: Auto-download failed: {e}")
        # Fallback: display download link with base64 data
        b64 = base64.b64encode(pdf_bytes).decode()
        display(HTML(
            f'<a download="{filename}" href="data:application/pdf;base64,{b64}">'
            f'Download {filename}</a>'
        ))
        return False


def pdf_from_html(pdf=None, verbose=False, no_header=False, attach=True, auto_save=True):
    """Export the current notebook as a PDF.

    Args:
        pdf: The name of the PDF to export (if None, uses notebook name)
        verbose: If True, print verbose output
        no_header: If True, skip adding timestamp/source header
        attach: If True, attach the .ipynb source file to the PDF
        auto_save: If True, save the notebook before exporting
    """
    if verbose:
        print("PDF via notebook_to_pdf")

    # Save notebook first if requested
    if auto_save:
        _save_notebook(verbose=verbose)

    # Check if we're in Colab
    if _is_colab():
        return _pdf_colab(pdf, verbose, no_header, attach)
    else:
        return _pdf_jupyter(pdf, verbose, no_header, attach)


def _pdf_colab(pdf_filename, verbose, no_header, attach):
    """Handle PDF export in Google Colab."""
    if verbose:
        print("Detected Google Colab environment")

    # Get notebook content from Colab
    nb_dict, nb_name = _get_colab_notebook()

    if nb_dict is None:
        print("Error: Could not retrieve notebook content from Colab.")
        print("Make sure you're running this in a Colab notebook.")
        return

    if verbose:
        print(f"Notebook: {nb_name}")

    # Convert dict to notebook node
    nb = nbformat.from_dict(nb_dict)

    # Normalize cell sources (Colab returns lists, nbconvert expects strings)
    nb = _normalize_cell_sources(nb)

    # Add header cell with metadata
    if not no_header:
        header_source = f'Generated at {time.asctime()}.'

        # Note about attachment
        if attach and _PYPDF_AVAILABLE:
            header_source += f'\n\n*Source notebook attached: {nb_name}.ipynb*'

        header_cell = nbformat.notebooknode.from_dict({
            'cell_type': 'markdown',
            'metadata': {},
            'source': header_source
        })
        nb['cells'].insert(0, header_cell)

    # Ensure chromium is installed
    _ensure_chromium()

    # Export to PDF
    if verbose:
        print("Exporting to PDF...")

    try:
        exporter = WebPDFExporter()
        body, resources = exporter.from_notebook_node(nb)
    except RuntimeError as e:
        if 'chromium' in str(e).lower():
            print("Error: Chromium not available for PDF export.")
            print("Try running: !playwright install chromium")
            return
        raise

    # Attach the notebook source if requested
    if attach:
        if verbose:
            print("Attaching notebook source...")
        body = _attach_notebook_to_pdf(body, nb_dict, f"{nb_name}.ipynb")

    # Determine filename
    if pdf_filename is None:
        pdf_filename = f"{nb_name}.pdf"
    elif not pdf_filename.endswith('.pdf'):
        pdf_filename += '.pdf'

    # Trigger download in Colab
    if verbose:
        print(f"Downloading: {pdf_filename}")

    _colab_download(body, pdf_filename)

    print(f"PDF exported: {pdf_filename}")
    if attach and _PYPDF_AVAILABLE:
        print(f"Attached: {nb_name}.ipynb")


def _pdf_jupyter(pdf_filename, verbose, no_header, attach):
    """Handle PDF export in Jupyter environments."""
    # Get notebook path
    notebook_path = get_notebook_path()
    if notebook_path is None:
        print("Error: Could not determine notebook path.")
        print("Make sure you're running in a Jupyter notebook.")
        return

    if verbose:
        print(f"Notebook: {notebook_path}")

    root_dir = os.path.dirname(notebook_path)
    nb_name = os.path.splitext(os.path.basename(notebook_path))[0]

    # Default PDF path
    if pdf_filename is None:
        base = os.path.splitext(notebook_path)[0]
        pdf_path = base + '.pdf'
    else:
        pdf_path = pdf_filename

    # Read notebook (keep original for attachment)
    with open(notebook_path) as f:
        nb_content = f.read()
    nb = nbformat.reads(nb_content, as_version=4)

    # Fix local image paths
    nb = _fix_local_images(nb, root_dir)

    # Add header cell with metadata
    if not no_header:
        header_source = f'Generated at {time.asctime()}.'

        # Add source link if we can determine URL
        source_url = _get_source_url(notebook_path)
        if source_url:
            header_source += f'\n\nSource: [{source_url}]({source_url})'

        # Note about attachment
        if attach and _PYPDF_AVAILABLE:
            header_source += f'\n\n*Source notebook attached: {nb_name}.ipynb*'

        header_cell = nbformat.notebooknode.from_dict({
            'cell_type': 'markdown',
            'metadata': {},
            'source': header_source
        })
        nb['cells'].insert(0, header_cell)

    # Ensure chromium is installed
    _ensure_chromium()

    # Export to PDF
    if verbose:
        print("Exporting to PDF...")

    try:
        exporter = WebPDFExporter()
        body, resources = exporter.from_notebook_node(nb)
    except RuntimeError as e:
        if 'chromium' in str(e).lower():
            print("Error: Chromium not available for PDF export.")
            print("Try running: !playwright install chromium")
            return
        raise

    # Attach the notebook source if requested
    if attach:
        if verbose:
            print("Attaching notebook source...")
        body = _attach_notebook_to_pdf(body, nb_content, f"{nb_name}.ipynb")

    with open(pdf_path, 'wb') as f:
        f.write(body)

    # Display download links
    rel_path = os.path.relpath(pdf_path, os.getcwd())
    display(Markdown(f'[Open {rel_path}]({rel_path})'))
    display(HTML(
        f'<a href="{rel_path}" download="{os.path.basename(rel_path)}">'
        f'Download {rel_path}</a>'
    ))

    if verbose:
        print(f"Saved: {pdf_path}")

    if attach and _PYPDF_AVAILABLE:
        print(f"Attached: {nb_name}.ipynb")


def pdf_from_latex(pdf=None, verbose=False, no_header=False, attach=True, auto_save=True):
    """Export the current notebook as a PDF using LaTeX.

    Requires a LaTeX installation (texlive, miktex, etc.).

    Args:
        pdf: The name of the PDF to export (if None, uses notebook name)
        verbose: If True, print verbose output
        no_header: If True, skip adding timestamp/source header
        attach: If True, attach the .ipynb source file to the PDF
        auto_save: If True, save the notebook before exporting
    """
    if not _LATEX_AVAILABLE:
        print("Error: LaTeX PDF export not available.")
        print("Install with: pip install nbconvert[webpdf]")
        print("Also requires a LaTeX installation (texlive, miktex, etc.)")
        return

    if verbose:
        print("PDF via LaTeX")

    # Save notebook first if requested
    if auto_save:
        _save_notebook(verbose=verbose)

    # Get notebook path
    notebook_path = get_notebook_path()
    if notebook_path is None:
        print("Error: Could not determine notebook path.")
        print("Make sure you're running in a Jupyter notebook.")
        return

    if verbose:
        print(f"Notebook: {notebook_path}")

    root_dir = os.path.dirname(notebook_path)
    nb_name = os.path.splitext(os.path.basename(notebook_path))[0]

    # Default PDF path
    if pdf is None:
        base = os.path.splitext(notebook_path)[0]
        pdf_path = base + '.pdf'
    else:
        pdf_path = pdf

    # Read notebook
    with open(notebook_path) as f:
        nb_content = f.read()
    nb = nbformat.reads(nb_content, as_version=4)

    # Fix local image paths
    nb = _fix_local_images(nb, root_dir)

    # Add header cell with metadata
    if not no_header:
        header_source = f'Generated at {time.asctime()}.'
        if attach and _PYPDF_AVAILABLE:
            header_source += f'\n\n*Source notebook attached: {nb_name}.ipynb*'

        header_cell = nbformat.notebooknode.from_dict({
            'cell_type': 'markdown',
            'metadata': {},
            'source': header_source
        })
        nb['cells'].insert(0, header_cell)

    # Export to PDF via LaTeX
    if verbose:
        print("Exporting to PDF via LaTeX...")

    exporter = PDFExporter()
    body, resources = exporter.from_notebook_node(nb)

    # Attach the notebook source if requested
    if attach:
        if verbose:
            print("Attaching notebook source...")
        body = _attach_notebook_to_pdf(body, nb_content, f"{nb_name}.ipynb")

    with open(pdf_path, 'wb') as f:
        f.write(body)

    # Display download links
    rel_path = os.path.relpath(pdf_path, os.getcwd())
    display(Markdown(f'[Open {rel_path}]({rel_path})'))
    display(HTML(
        f'<a href="{rel_path}" download="{os.path.basename(rel_path)}">'
        f'Download {rel_path}</a>'
    ))

    if verbose:
        print(f"Saved: {pdf_path}")

    if attach and _PYPDF_AVAILABLE:
        print(f"Attached: {nb_name}.ipynb")


def pdf(line=""):
    """Line magic to export a notebook to PDF.

    Usage:
        %pdf                  - Export to notebook-name.pdf (with .ipynb attached)
        %pdf output.pdf       - Export to specific filename
        %pdf -v               - Verbose output
        %pdf --html           - Use HTML/WebPDF export (default, uses Playwright)
        %pdf --latex          - Use LaTeX export (requires texlive/miktex)
        %pdf --no-header      - Skip timestamp/source header
        %pdf --no-attach      - Don't attach the .ipynb source file
        %pdf --no-save        - Don't auto-save notebook before export

    Examples:
        %pdf
        %pdf my-report.pdf
        %pdf -v --no-header
        %pdf --latex my-report.pdf
        %pdf --html --no-attach
    """
    args = shlex.split(line)

    # Parse flags
    verbose = '-v' in args or '--verbose' in args
    use_latex = '--latex' in args
    no_header = '--no-header' in args
    attach = '--no-attach' not in args  # Attach by default
    auto_save = '--no-save' not in args  # Auto-save by default

    # List of known flags to skip when looking for filename
    known_flags = ('--html', '--latex', '--no-header', '--no-attach', '--no-save', '--verbose', '-v')

    # Find output filename from args
    pdf_name = None
    for arg in args:
        if arg.endswith('.pdf'):
            pdf_name = arg
            break
        # Also accept filename without .pdf extension
        if not arg.startswith('-') and arg not in known_flags:
            if pdf_name is None:
                pdf_name = arg

    # Add .pdf extension if not present
    if pdf_name and not pdf_name.endswith('.pdf'):
        pdf_name = pdf_name + '.pdf'

    # Choose export method
    if use_latex:
        pdf_from_latex(pdf_name, verbose, no_header, attach, auto_save)
    else:
        pdf_from_html(pdf_name, verbose, no_header, attach, auto_save)


# Register the magic command
try:
    pdf = register_line_magic(pdf)
except:
    pass
