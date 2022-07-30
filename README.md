# coppertop-bones-demo

Jupyter notebooks and other examples using coppertop-bones. 

Use this - https://nbviewer.jupyter.org - if github doesn't render properly. 

E.g. https://nbviewer.jupyter.org/github/DangerMouseB/coppertop-bones-demo/blob/main/jupyter/think%20bayes/Ch%201%2C2%2C3%20-%20models.ipynb


<br>

#### Notebook dependencies and coppertop

I have matplotlib, plotnine, numpy, pandas, scipy, pymc3, etc, installed.

Install coppertop-bones-demo via `python -m pip install coppertop-bones-demo`. This also installs coppertop-bones.

Alternatively clone https://github.com/DangerMouseB/coppertop-bones and https://github.com/DangerMouseB/coppertop-bones-demo 
and ensure your PYTHONPATH is set to include the src folders, for example:

```
/Users/david/repos/github/DangerMouseB/coppertop-bones/src 
/Users/david/repos/github/DangerMouseB/coppertop-bones-demo/src
```

Alternatively, you can manually set `sys.path` to include the coppertop-bones/src folder and then at the top of a 
notebook you can do the following:

```
from coppertop.core import ensurePath
'/Users/david/repos/github/DangerMouseB/coppertop-bones-demo/src' >> ensurePath       # <= set this to your path
```

The notebook should be good to go.

