from .manager import PermissionManager
from .cli import app

class HVPDBPermsPlugin(PermissionManager):
    app = app
__all__ = ['PermissionManager', 'app', 'HVPDBPermsPlugin']