# nothing
import os

from confuse import Configuration

cfg = Configuration('pyunifi', __name__)


class PYUnifiIOError(OSError):
    """A pyunifi IO error"""


class PYUnifiError(Exception):
    """A pyunifi standard error"""


def getlogininfo(username: str = "", password: str = "", hostname: str = ""):
    """
    helper function to get login
    prio: args > os env var > configfile
    """
    if username != "" and password != "" and hostname != "":
        return
    UNIFI_USER = None
    UNIFI_PASSWORD = None
    UNIFI_HOSTNAME = None
    if os.environ.get('UNIFI_USER', None) != None:
        UNIFI_USER = os.environ.get('UNIFI_USER', None)
        UNIFI_PASSWORD = os.environ.get('UNIFI_PASSWORD', None)
        UNIFI_HOSTNAME = os.environ.get('UNIFI_HOSTNAME', None)
    else:
        if 'username' in cfg and 'password' in cfg:
            UNIFI_USER = cfg['username']
            UNIFI_PASSWORD = cfg['password']
            UNIFI_HOSTNAME = cfg['hostname']
    return UNIFI_USER, UNIFI_PASSWORD, UNIFI_HOSTNAME


class APIKeyMissingError(Exception):
    pass


from .trafficrule import TrafficRule
from .unificontroller import UnifiController
