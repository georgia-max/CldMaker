# Causual Loop Diagram Maker 

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)

## Overview

The process of transforming a Dynamic Hypothesis into a Casual Loop Diagram (CLD) that articulates the casual strucuture of the system is a key step in the development of System Dynamics (SD) models. In this repository, we present a method for automating the translation of dynamic hypothesis (text) into CLDs using Large Language Models. 


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Trouble Shootings](#troubleshooting)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)


## Installation

1. Clone the repository:

    ```bash
    https://github.com/georgia-max/CldMaker.git
    ```
2. Activate virtual environment in your terminal:
   ```
    source venv/bin/activate
    ```
3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```


## Usage


## Example

```python
python ./main.py
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
