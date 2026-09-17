import warnings
from rich.markdown import Markdown
from rich.traceback import install, Traceback
from rich import print
import key_multivalue_storage as kms

install(show_locals=True)

try:
    kms.test_nextgen()
except TypeError as e:
    print(Markdown(str(e)))
except Exception as e:
    warnings.warn(f"An unexpected exception occurred: {e}")

kms.nextgen = True

kms.test_nextgen()
