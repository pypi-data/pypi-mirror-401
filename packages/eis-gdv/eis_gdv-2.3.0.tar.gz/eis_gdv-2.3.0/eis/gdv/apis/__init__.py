
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from eis.gdv.api.health_api import HealthApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from eis.gdv.api.health_api import HealthApi
from eis.gdv.api.mailbox_api import MailboxApi
from eis.gdv.api.messages_api import MessagesApi
from eis.gdv.api.users_api import UsersApi
from eis.gdv.api.vbas_api import VbasApi
from eis.gdv.api.vbus_api import VbusApi
from eis.gdv.api.zip_codes_api import ZipCodesApi
