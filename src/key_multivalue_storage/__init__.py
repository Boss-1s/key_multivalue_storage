"""
## `key_multivalue_storage` - a PyPI package also known as kms.

kms is a *simple, yet growing,* **JSON wrapper library** that **allows the JSON storage of one key
to multiple values.**

### Made with love by Boss_1s.

-------

## Original Docstring
Basically a nested-dictionary (key to key-value) ~~module~~ library I made because
**I didn't like how scratchattach's database worked and the steep learning curve
that came with it.**

So far, this is the ***greatest piece of a python program I have ever made.***
"""
# Built-ins
import sys
import warnings
import inspect
from typing import Any, Callable

# Third-party
from rich.console import Console, Group
from rich.syntax import Syntax
from rich.panel import Panel
from rich.markdown import Markdown
from rich.tree import Tree
from rich.traceback import install

# First-party
# Modules
from . import storage
from . import load
from . import edit
from . import delete

# Classes
from .storage import Storage
from .load import Load
from .edit import Edit
from .delete import Delete

# Custom Warnings and Exceptions
from .utils import exceptions as kms_exceptions
from .utils import warnings as kms_warnings

from .utils.exceptions import KeyNotFoundError, NoInstantiationError
from .utils.warnings import DeleteWarning, AdditionFailureWarning, SubtractionFailureWarning, CastWarning

__version__ = "v1.3.0.20260730"
__version_internal__ = "kms-v1.3.0/2026.07.30"
__author__ = "Boss_1s"
__license__ = "GPLv2"

kms = storage
key_multivalue_storage = storage

__all__ = [
    "Storage", # main class object Storage
    "Load", # Load class
    "Edit", # Edit class
    "Delete", # Delete class
    "kms_exceptions", # custom exceptions
    "kms_warnings", # custom warnings
]

warnings.filterwarnings("always",
                        category=PendingDeprecationWarning,
                        module="key_multivalue_storage")
warnings.filterwarnings("always",
                        category=DeprecationWarning,
                        module="key_multivalue_storage")

install(show_locals=True)

warnings.warn("Going from kms-semver2.0, the module "+
              "name 'key_multivalue_storage' will be deprecated "+
              "in favor of the name 'kms'. Please note this "+
              "change accordingly, thank you! See the documentation "+
              "for more information.",
              PendingDeprecationWarning,
              stacklevel=5
             )

# NOTE: Warn in like v1.5 or smth
#warnings.warn("kms-v1.x will be officially discontinued soon."+
#              "The last major content update will be kms-v1.6, most "+
#              "likely around the time kms-v2.1 comes out. Please "+
#              "stay tuned to avoid version compatibility conflicts.",
#              PendingDeprecationWarning
#             )

def help() -> None: #pylint: disable=redefined-builtin
    """Beautiful help panel created with Rich."""
    from . import load, edit, delete #pylint: disable=import-outside-toplevel
    def _add_to_tree(tree: Tree, method: Callable[..., Any]) -> None:
        """
        Add a method to the tree with its signature and docstring.

        ### Args
            tree (Tree): The tree to which the method will be added.
            method (Callable[..., Any]): The method to add to the tree.
        """
        annotation_str: str = '('
        for arg, typ in method.__annotations__.items():
            if arg == 'return':
                if annotation_str.endswith(", "):
                    annotation_str = annotation_str[:-2]
                annotation_str += f") -> {typ}"
            else:
                annotation_str = annotation_str + f"{arg}: {typ}"
                if inspect.signature(method).parameters[arg]:
                    default = inspect.signature(method).parameters[arg].default
                    if default is not inspect.Parameter.empty:
                        annotation_str += f"={default}"
                annotation_str += ", "

        signature = f"def {method.__name__}{annotation_str}: ..,."
        docstring = Markdown(str(method.__doc__)) if method.__doc__ else "[red]No docstring available.[/]"

        tree.add(
            Group(
                Syntax(signature, "python"),
                docstring
            ),
            guide_style="red"
        )

    console = Console()

    orange: str = "#ff5533"

    library = Tree("[b blue]kms", highlight=True, guide_style="blue")

    utils = library.add("[green]utils", guide_style="green")

    kms_exceptions = utils.add("[cyan]exceptions.py", guide_style="cyan")
    kms_exceptions.add(
        Group(
            Syntax(
                "class KeyNotFoundError(KeyError) -> None: ...", "python"
            ),
            str(exceptions.KeyNotFoundError.__doc__).strip()
        ),
        guide_style=orange
    )
    kms_exceptions.add(
        Group(
            Syntax(
                "class NoInstantiationError(KeyError) -> None: ...", "python"
            ),
            str(exceptions.NoInstantiationError.__doc__).strip()
        ),
        guide_style=orange
    )

    utils.add("[cyan]metadata.py", guide_style="cyan")

    w = utils.add("[cyan]warnings.py", guide_style="cyan")
    w.add(
        Group(
            Syntax(
                "class DeleteWarning(UserWarning) -> None: ...", "python"
            ),
            str(kms_warnings.DeleteWarning.__doc__).strip()
        ),
        guide_style=orange
    )
    w.add(
        Group(
            Syntax(
                "class AdditionFailureWarning(UserWarning) -> None: ...", "python"
            ),
            str(kms_warnings.AdditionFailureWarning.__doc__).strip()
        ),
        guide_style=orange
    )
    w.add(
        Group(
            Syntax(
                "class SubtractionFailureWarning(UserWarning) -> None: ...", "python"
            ),
            str(kms_warnings.SubtractionFailureWarning.__doc__).strip()
        ),
        guide_style=orange
    )
    w.add(
        Group(
            Syntax(
                "class CastWarning(UserWarning) -> None: ...", "python"
            ),
            str(kms_warnings.CastWarning.__doc__).strip()
        ),
        guide_style=orange
    )

    init = library.add("[b blue]__init__.py")
    _add_to_tree(init, help)

    store = library.add("[cyan]storage.py", guide_style="cyan")
    _add_to_tree(store, storage.help)
    s = store.add(
        Group(
            Syntax(
                "@total_ordering\n"+
                "class Storage(metaclass=.utils.metadata._StorageMeta) -> Storage: ...",
                "python"
            ),
            Markdown(str(Storage.__doc__))
        ),
        guide_style=orange
    )
    _add_to_tree(s, Storage.help)
    _add_to_tree(s, Storage.store)

    load_module = library.add("[cyan]load.py", guide_style="cyan")
    _add_to_tree(load_module, load.help)
    load_cls = load_module.add(
        Group(
            Syntax(
                "class Load(metaclass=.utils.metadata._LoadMeta) -> None: ...",
                "python"
            ),
            Markdown(str(Load.__doc__))
        ),
        guide_style=orange
    )
    _add_to_tree(load_cls, Load.help)
    _add_to_tree(load_cls, Load.by_key)
    _add_to_tree(load_cls, Load.by_index)
    _add_to_tree(load_cls, Load.keys)
    _add_to_tree(load_cls, Load.values)

    edit_module = library.add("[cyan]edit.py", guide_style="cyan")
    _add_to_tree(edit_module, edit.help)
    edit_cls = edit_module.add(
        Group(
            Syntax(
                "class Edit(metaclass=.utils.metadata._EditMeta) -> None: ...",
                "python"
            ),
            Markdown(str(Edit.__doc__))
        ),
        guide_style=orange
    )
    _add_to_tree(edit_cls, Edit.help)
    _add_to_tree(edit_cls, Edit.propval)
    _add_to_tree(edit_cls, Edit.propkey)
    _add_to_tree(edit_cls, Edit.key)

    delete_module = library.add("[cyan]delete.py", guide_style="cyan")
    _add_to_tree(delete_module, delete.help)
    delete_cls = delete_module.add(
        Group(
            Syntax(
                "class Delete(metaclass=.utils.metadata._DeleteMeta) -> None: ...",
                "python"
            ),
            Markdown(str(Delete.__doc__))
        ),
        guide_style=orange
    )
    _add_to_tree(delete_cls, Delete.help)
    _add_to_tree(delete_cls, Delete.by_propkey)
    _add_to_tree(delete_cls, Delete.by_key)
    _add_to_tree(delete_cls, Delete.all)

    legend_text = Group(
        """[b blue]Blue - Top level module[/b blue]
[green]Green - Sub-module (folder)[/]
[cyan]Cyan - Module (file)[/]
[#ff5533]Orange - Class[/]
[red]Red - Method[/]

[i]Private APIs (ones starting with '_') and dunder methods like __init__ are not included.""",
        Markdown("**For more details about those specific methods and classes, "+
                "see the [documentation]"+
                "(https://boss-1s.github.io/key_multivalue_storage/Documentation).**"
        )
    )

    legend = Panel.fit(legend_text, title="Key")

    console.print(
        Markdown(
            "# Key to Multivalue Storage (key_multivalue_storage, kms)"
        ),
        Markdown(str(__doc__))
    )

    if hasattr(sys, 'ps1'):
        console.print("\n[b green]Hit enter to continue[/b green]")

        input()

    console.print(
        Markdown("--------\n## Structure of the Library"),
        legend,
        library,
        sep="\n"
    )
