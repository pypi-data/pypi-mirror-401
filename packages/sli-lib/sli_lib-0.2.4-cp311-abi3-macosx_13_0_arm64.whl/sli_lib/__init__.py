"""

# Introduction

sli-lib is a library for manipulating and using the FO(·) language using the rust sli-lib library.
sli-lib contains two major parts the `fodot` module for representing and manipulating FO(·) and the `solver` module for executing inference tasks on FO(·) theories.

# `fodot`

The `fodot` module contains three modules `vocabulary`, `theory` and `structure`.
Each containing datastructures and method for representing FO(·) constructs for vocabularies, theories and structures respectively.

# `solver`

In the `solver` module, solver implementations can be found and used with an `sli_lib.fodot.knowledge_base.Inferenceable` object.
Each solver implements some inference tasks over this knowledge base such as, satisfiability check, model expansion, back-bone propagation, ...

# `methods`

In the `methods` module some useful inference task functions can be found that don't require the more flexible but boilerplate prone approach of creating an `sli_lib.fodot.knowledge_base.Inferenceable` then using this in an `sli_lib.solver.Z3Solver`.

# Example

```python
from sli_lib.fodot import Vocabulary, Structure, Theory, Inferenceable
from sli_lib.fodot.structure import StrInterp
from sli_lib.solver import Z3Solver

# Create a vocabulary
vocab = Vocabulary()
vocab.add_type("Node")
vocab.add_type("Color")
vocab.add_pfunc("edge", ("Node", "Node"), "Bool")
vocab.add_pfunc("colorOf", ("Node",), "Color")
# Create a theory
theory = Theory(vocab)
theory.parse("!x, y in Node: edge(x, y) => colorOf(x) ~= colorOf(y).")
# Create a structure
struct = Structure(vocab)
struct.set_type_interp("Node", StrInterp(f"a{i}" for i in range(20)))
struct.set_type_interp("Color", StrInterp(["red", "green", "blue"]))
# Add some edges to struct
edge = struct["edge"]
for args in [
    ("a1", "a2"),
    ("a1", "a3"),
    ("a3", "a2"),
    ("a1", "a4"),
    ("a2", "a4"),
    ("a3", "a4"),
]:
    edge.set(args, True)
edge.set_all_unknown_to_value(False)
# Put our theory and structure together in an Inferenceable and ask for satisfiability from Z3Solver
inferenceable = Inferenceable(theory, struct)
solver = Z3Solver(inferenceable)
assert not solver.check() # this instance of graph colouring is unsatisfiable
```

# Pyodide build

Each SLI release since 0.2.2 builds and releases a Pyodide wheel in the SLI repository.
This wheel allows sli-lib to run on most (modern) Javascript interpreters that support web assembly, notably browsers.
These wheels can be used to install and run SLI in Pyodide.

A URL to such a wheel file can be used together with Pyodide's micropip library to install sli-lib, do note that when running Pyodide on browsers this URL must set correct CORS headers otherwise this function will fail, see <https://pyodide.org/en/stable/usage/loading-packages.html#installing-wheels-from-arbitrary-urls> for more info.
The gitlab package registry URLs are suitable for installing sli-lib from the browser, these wheels have names that match the following regular expression `sli_lib-.*-emscripten_.*_wasm32.whl` and can be found on the SLI repository release page <https://gitlab.com/sli-lib/SLI/-/releases>.

Installing sli-lib into a Pyodide interpreter is done using the following code together with such a URL:

```python
import micropip # @no-test
sli_lib_wheel_url = ...
await micropip.install(sli_lib_wheel_url)
```

From Javascript this would look like the following, with `pyodide` being a [Pyodide api object](https://pyodide.org/en/stable/usage/api/js-api.html#js-api-pyodide).

```javascript
await pyodide.loadPackage('micropip'); // make sure micropip is available!
sli_lib_wheel_url = "...";
await pyodide.runPythonAsync(`import micropip; await micropip.install("${sli_lib_url}");`);
```

For documentation on how to use Pyodide see <https://pyodide.org/en/stable/>.

# Free threading support

sli-lib does not rely on the Python global interpreter lock.
As such it fully supports free threaded Python.
Just like the builtin Python types, the sli-lib types, where needed, add locks to prevent memory unsafety and data races.
Do note that this requires building the api explicitly targeting free-threaded python.

"""

from .sli_lib import * # type: ignore[import-not-found]
from . import fodot as fodot
from . import solver as solver
from . import methods as methods
from sli_lib.fodot.knowledge_base import KnowledgeBase, Procedure
import sys

def script_main():
    import sys
    sli_cli_main(sys.argv, True, False)


def _exec(procedure: str, kb_file: str):
    if kb_file == "-":
        kb_str = sys.stdin.read()
    else:
        with open(kb_file) as file:
            kb_str = file.read()
    kb = KnowledgeBase.from_str(kb_str)
    try:
        block = kb[procedure]
    except KeyError:
        print(f"error: No procedure with name {procedure} found.", file=sys.stderr)
        exit(1)
    if isinstance(block, Procedure):
        block()
    else:
        print(f"error: Cannot execute a {type(block).__name__.lower()}", file=sys.stderr)
        exit(1)


# Keep this up to date manually
__all__ = [
    "fodot",
    "solver",
    "methods",
]
