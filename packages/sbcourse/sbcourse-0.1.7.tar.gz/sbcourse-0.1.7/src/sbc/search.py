"""Search functionality for Jupyter notebooks using ChromaDB."""

import os
import json
import glob
import argparse

import chromadb
import nbformat
from tqdm import tqdm
from nbconvert import MarkdownExporter
from IPython.core.magic import register_cell_magic, register_line_magic
from IPython.display import Markdown, display

from .config import config

# Module-level storage for lazy-loaded database
_db = None
_collection = None


def notebook_to_markdown(notebook_path):
    """Convert a Jupyter notebook to markdown string.

    Args:
        notebook_path: Path to the notebook file

    Returns:
        str: Markdown representation of the notebook
    """
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    # Create a Markdown exporter
    markdown_exporter = MarkdownExporter()

    # Convert the notebook to a markdown string
    markdown_string, _ = markdown_exporter.from_notebook_node(notebook)

    return markdown_string


def initialize_search_db(dbfile=None,
                         collection_name=None,
                         root=None,
                         pattern=None,
                         exclude_patterns=None):
    """Initialize or load the ChromaDB search database.

    Args:
        dbfile: Path to the ChromaDB database file (default from config)
        collection_name: Name of the collection to use (default from config)
        root: Root directory for computing relative paths (default from config)
        pattern: Glob pattern for finding notebooks (default from config)
        exclude_patterns: List of patterns to exclude (default from config)

    Returns:
        tuple: (db, collection) - ChromaDB client and collection objects
    """
    # Use config defaults if not provided
    if dbfile is None:
        dbfile = config.paths.search_db
    if collection_name is None:
        collection_name = config.paths.search_collection
    if root is None:
        root = config.paths.notebook_root
    if pattern is None:
        pattern = os.path.join(config.paths.notebook_root, config.search.include_pattern)
    if exclude_patterns is None:
        exclude_patterns = config.search.exclude_patterns

    dbfile = os.path.expanduser(dbfile)
    root = os.path.expanduser(root)
    pattern = os.path.expanduser(pattern)

    if not os.path.exists(dbfile):
        db = chromadb.PersistentClient(path=dbfile)
        if collection_name in [c.name for c in db.list_collections()]:
            db.delete_collection(collection_name)

        collection = db.get_or_create_collection(collection_name)
        print('Indexing files. It should not take long, and it should only happen once.')

        for fullpath in tqdm(glob.glob(pattern, recursive=True)):
            # Skip excluded patterns
            if any(excl in fullpath for excl in exclude_patterns):
                continue

            mdcounter, codecounter = 0, 0
            with open(fullpath) as f:
                ipynb = json.loads(f.read())
                for cell in ipynb['cells']:
                    if cell["cell_type"] == "markdown":
                        text = ''.join(cell['source'])
                        path = os.path.relpath(fullpath, start=root)
                        # Build URL using config
                        github_repo = f'{config.course.github_org}/{config.course.github_repo}'
                        course_name = config.course.name
                        url = f'[{path} :markdown: {mdcounter}]({config.jupyterhub.base_url}/hub/user-redirect/git-pull?repo=https%3A//{github_repo}&urlpath=lab/tree/{course_name}/{path}&branch={config.course.github_branch})'
                        collection.add(documents=[text], ids=[url])
                        mdcounter += 1
                    elif cell["cell_type"] == "code":
                        text = ''.join(cell['source'])
                        path = os.path.relpath(fullpath, start=root)
                        # Build URL using config
                        github_repo = f'{config.course.github_org}/{config.course.github_repo}'
                        course_name = config.course.name
                        url = f'[{path} :code: {codecounter}]({config.jupyterhub.base_url}/hub/user-redirect/git-pull?repo=https%3A//{github_repo}&urlpath=lab/tree/{course_name}/{path}&branch={config.course.github_branch})'
                        collection.add(documents=[text], ids=[url])
                        codecounter += 1
    else:
        db = chromadb.PersistentClient(path=dbfile)
        collection = db.get_or_create_collection(collection_name)

    return db, collection


def _get_collection():
    """Get the search collection, loading from disk if available."""
    global _db, _collection

    if _collection is not None:
        return _collection

    dbfile = os.path.expanduser(config.paths.search_db)
    collection_name = config.paths.search_collection

    if os.path.exists(dbfile):
        _db = chromadb.PersistentClient(path=dbfile)
        _collection = _db.get_or_create_collection(collection_name)
        return _collection

    return None


def index(line=""):
    """Line magic to build the search index.

    Usage:
        %index           - Build the search index for course notebooks
        %index --rebuild - Force rebuild of the index
    """
    global _db, _collection

    rebuild = '--rebuild' in line or '-r' in line
    dbfile = os.path.expanduser(config.paths.search_db)

    if os.path.exists(dbfile) and not rebuild:
        print(f"Search index already exists at {dbfile}")
        print("Use %index --rebuild to force rebuild")
        _db, _collection = initialize_search_db()
        return

    if rebuild and os.path.exists(dbfile):
        import shutil
        shutil.rmtree(dbfile)
        print("Removed existing index.")

    print("Building search index...")
    _db, _collection = initialize_search_db()
    print("Search index built successfully.")


def search(line, cell):
    """Cell magic to search for notebooks related to a query.

    Usage:
        %%search -n 5
        What is a Gaussian process?

    Args:
        line: Command line arguments (-n for number of results)
        cell: The search query text
    """
    collection = _get_collection()

    if collection is None:
        print("Error: Search index not found.")
        print("Run %index to build the search index first.")
        return

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=3, help='Number of documents to return')
    args = parser.parse_args(line.split())

    prompt = cell
    results = collection.query(query_texts=[prompt], n_results=args.n)

    print('The closest notebooks are:')
    for i, (url, doc) in enumerate(zip(results['ids'][0], results['documents'][0]), 1):
        display(Markdown(f'{i}. ' + url))
        if ':markdown:' in url:
            display(Markdown(doc))
        elif ':code:' in url:
            display(Markdown(f'```python\\n{doc}\\n```'))


# Register magic commands
try:
    index = register_line_magic(index)
    search = register_cell_magic(search)
except:
    pass
