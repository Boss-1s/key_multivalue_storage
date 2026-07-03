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
import warnings
from rich.console import Console, Group
from rich.syntax import Syntax
from rich.panel import Panel
from rich.markdown import Markdown
from rich.tree import Tree
from rich.traceback import install

from . import storage

from .storage import Storage
from .load import Load
from .edit import Edit
from .delete import Delete

from .utils import exceptions
from .utils import warnings as kms_warnings

__version__ = "v1.3.0.20260703a4"
__version_internal__ = "kms-v1.3.0a4/2026.07.03"
__author__ = "Boss_1s"
__license__ = "GPLv2"

kms = storage
key_multivalue_storage = storage

__all__ = [
    "key_multivalue_storage", # full name
    "kms", # short name
    "Storage", # main class object Storage
    "Load", # Load class
    "Edit", # Edit class
    "Delete", # Delete class
    "exceptions", # custom exceptions
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

def help() -> None:
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
    init.add(
        Group(
            Syntax(
                "def help() -> None: ...", "python"
            ),
            ""
        ),
        guide_style="red"
    )

    store = library.add("[cyan]storage.py", guide_style="cyan")
    store.add(
        Group(
            Syntax(
                "def help() -> None: ...", "python"
            ),
            str(kms.help.__doc__)
        ),
        guide_style="red"
    )
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
    s.add(
        Group(
            Syntax(
                "def help(method: ((Any) -> Any) | None) -> None: ...", "python"
            ),
            str(Storage.help.__doc__)
        ),
        guide_style="red"
    )
    s.add(
        Group(
            Syntax(
                """def store(
    self: Storage,
    file_path: str,
    instant_delete: bool | None = None,
    indent: int | None = None,
    encode: bool | None = None
) -> None: ...""",
                "python"
            ),
            str(Storage.store.__doc__).strip()
        ),
        guide_style="red"
    )
    load = library.add("[cyan]load.py", guide_style="cyan")
    load.add("[b green]Docs Coming Soon!")
    edit = library.add("[cyan]edit.py", guide_style="cyan")
    edit.add("[b green]Docs Coming Soon!")
    delete = library.add("[cyan]delete.py", guide_style="cyan")
    delete.add("[b green]Docs Coming Soon!")

    legend_text = """[b blue]Blue - Top level module[/b blue]
[green]Green - Sub-module (folder)[/]
[cyan]Cyan - Module (file)[/]
[#ff5533]Orange - Class[/]
[red]Red - Method[/]

[i]Private APIs and dunder methods like __init__ are not included.
For more details about those specific methods and classes, see the documentation.
"""
    legend = Panel.fit(legend_text, title="**Key**")

    console.print(
        Markdown(
            "# Key to Multivalue Storage (key_multivalue_storage, kms)"
        ),
        Markdown(str(__doc__)),
        Markdown("--------\n## Structure of the Library"),
        legend,
        library,
        sep="\n"
    )
