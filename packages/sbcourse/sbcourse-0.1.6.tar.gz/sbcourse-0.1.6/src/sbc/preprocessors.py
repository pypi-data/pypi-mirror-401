'''nbconvert preprocessors

At the command line use this:

jupyter nbconvert --to notebook --NotebookExporter.preprocessors=sbc.ReleasePreprocessor introduction.ipynb --output test
'''

import re
from nbconvert.preprocessors import Preprocessor
from nbconvert.preprocessors import ClearOutputPreprocessor


class SolutionPreprocessor(Preprocessor):
    '''Remove SOLUTION fences, but leave content
    
    Assumes these are all in one cell, i.e. they do not span cells.
    '''
    
    def preprocess(self, nb, resources):  
        
        # These are usually in code cells
        solution_rx = '''### BEGIN SOLUTION
((.|\n)*)
### END SOLUTION'''
        
        # This is for markdown cells. The pattern above is not nice for 
        # marking because it looks like a heading.
        solution_md = '''<!-- BEGIN SOLUTION -->
((.|\n)*)
<!-- END SOLUTION -->
```'''
        
        for cell in nb.cells:
            s = ''.join(cell['source'])
            if cell['cell_type'] == 'code':
                m = re.search(solution_rx, s)
                if m:
                    s = s.replace(m.group(0), m.group(1))
            elif cell['cell_type'] == 'markdown':
                m = re.search(solution_md, s)
                if m:
                    s = s.replace(m.group(0), m.group(1))
            else:
                raise Exception(f'Cell type {cell["cell_type"]} is not supported yet.')
                     
            # remove solutions, and put \n back on each line.
            cell['source'] = [x + '\n' for x in s.strip().split('\n')]
           
        return nb, resources

    
class RemoveSolutionPreprocessor(Preprocessor):
    '''Remove SOLUTION fences.
    
    Assumes these are all in one cell, i.e. they do not span cells.
    '''
    
    def preprocess(self, nb, resources):  
        
        # These are usually in code cells
        solution_rx = '''### BEGIN SOLUTION
((.|\n)*)
### END SOLUTION'''
        
        # This is for markdown cells. 
        solution_md = '''<!-- BEGIN SOLUTION -->
((.|\n)*)
<!-- END SOLUTION -->
'''
        
        for cell in nb.cells:
            s = ''.join(cell['source'])
            
            if cell['cell_type'] == 'code':
                s = re.sub(solution_rx, '', s)
            elif cell['cell_type'] == 'markdown':
                # The rx isn't working above and I need to get on with the day for now.
                if "BEGIN SOLUTION" in s:
                    s = ""
                #s = re.sub(solution_md, '', s)
            else:
                raise Exception(f'Cell type {cell["cell_type"]} is not supported yet.')
                     
            # remove solutions, and put \n back on each line.
            cell['source'] = [x + '\n' for x in s.split('\n')]
           
        return nb, resources
    
    
class HiddenPreprocessor(Preprocessor):
    '''Remove HIDDEN fences and hidden cells.
    
    Assumes these are all in one cell, i.e. they do not span cells.
    '''
    
    def preprocess(self, nb, resources):
        hidden_rx = '''### BEGIN HIDDEN
((.|\n)*)
### END HIDDEN'''
        
        todelete = []
        
        for i, cell in enumerate(nb.cells): 
            # Track tagged cells and delete later.
            if 'hidden' in cell.metadata.get('tags', []):
                todelete += [i]
                
            s = ''.join(cell['source'])
            s = re.sub(hidden_rx, '', s)
        
            # remove solutions, and put \n back on each line.
            cell['source'] = [x + '\n' for x in s.split('\n')]
            
        # These were tagged hidden
        for i in sorted(todelete, reverse=True):
            del nb.cells[i]
            
        return nb, resources
    
class ReleasePreprocessor(Preprocessor): 
    """Combine the processors.

    """
    def preprocess(self, nb, resources):
        pp = [ClearOutputPreprocessor, HiddenPreprocessor, SolutionPreprocessor]
        for p in pp:
            nb, resources = p().preprocess(nb, resources)
        return nb, resources