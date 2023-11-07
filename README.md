# Set up virtual enviroment 

First, activate virtual environment in your terminal
```
source venv/bin/activate
```

Second, install libraries in the virtual environment 

```
pip install -r requirements.txt
```

## Trouble Shootings
Error when render Graphviz
```
if e.errno == errno.ENOENT:
>               raise ExecutableNotFound(cmd) from e
E               graphviz.backend.execute.ExecutableNotFound: failed to execute PosixPath('dot'), make sure the Graphviz executables are on your systems' PATH

../../venv/lib/python3.11/site-packages/graphviz/backend/execute.py:84: ExecutableNotFound
```
Cause: Graphviz executables are not in developer's local machine \
Solution: 
in Mac
```commandline
brew install graphviz
```
reference: https://www.graphviz.org/download/