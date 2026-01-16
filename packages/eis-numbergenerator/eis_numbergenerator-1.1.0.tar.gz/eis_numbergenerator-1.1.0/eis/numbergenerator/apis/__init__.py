
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from eis.numbergenerator.api.numbers_api import NumbersApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from eis.numbergenerator.api.numbers_api import NumbersApi
from eis.numbergenerator.api.default_api import DefaultApi
