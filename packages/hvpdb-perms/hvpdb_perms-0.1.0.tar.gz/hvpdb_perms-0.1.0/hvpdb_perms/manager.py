from typing import Optional
from hvpdb.core import HVPDB

class PermissionManager:

    def __init__(self, db: HVPDB):
        self.db = db

    def _is_root(self, username: str) -> bool:
        return username == 'root'

    def _is_admin(self, user_data: dict) -> bool:
        return user_data.get('role') == 'admin'

    def _can_manage_group(self, user_data: dict, group_name: str) -> bool:
        user_groups = user_data.get('groups', [])
        return '*' in user_groups or group_name in user_groups

    def _check_access(self, required_group: str=None):
        caller = getattr(self.db, 'current_user', None)
        if not caller or self._is_root(caller):
            return
        caller_data = self.db.storage.data['users'].get(caller)
        if not caller_data:
            raise PermissionError('Access Denied: Caller not found.')
        if self._is_admin(caller_data):
            return
        if required_group is None:
            raise PermissionError('Access Denied: Only Root/Admin can perform this action.')
        if self._can_manage_group(caller_data, required_group):
            return
        raise PermissionError(f"Access Denied: You do not have permission to manage group '{required_group}'.")

    def create_user(self, username: str, password: str, role: str='user'):
        if username == 'root':
            raise ValueError('Root user cannot be created or modified.')
        if self.db.is_cluster:
            raise NotImplementedError('User management not supported in cluster mode yet.')
        if 'users' not in self.db.storage.data:
            self.db.storage.data['users'] = {}
        if username in self.db.storage.data['users']:
            raise ValueError(f"User '{username}' already exists.")
        caller = getattr(self.db, 'current_user', None)
        if not caller or self._is_root(caller):
            pass
        else:
            caller_data = self.db.storage.data['users'].get(caller)
            if not caller_data:
                raise PermissionError('Access Denied: Caller not found.')
            caller_role = caller_data.get('role', 'user')
            if caller_role == 'user':
                raise PermissionError('Access Denied: Users cannot create other users.')
            if caller_role == 'manager':
                if role in ('admin', 'manager'):
                    raise PermissionError("Access Denied: Managers can only create 'user' role.")
        self.db.storage.data['users'][username] = {'password': password, 'role': role, 'groups': []}
        self.db.storage._dirty = True

    def grant(self, username: str, group_name: str):
        self._check_access(group_name)
        if username not in self.db.storage.data['users']:
            raise ValueError(f"User '{username}' not found.")
        user_data = self.db.storage.data['users'][username]
        if group_name not in user_data['groups']:
            user_data['groups'].append(group_name)
            self.db.storage._dirty = True

    def revoke(self, username: str, group_name: str):
        self._check_access(group_name)
        if username not in self.db.storage.data['users']:
            raise ValueError(f"User '{username}' not found.")
        user_data = self.db.storage.data['users'][username]
        if group_name in user_data['groups']:
            user_data['groups'].remove(group_name)
            self.db.storage._dirty = True

    def list_users(self):
        self._check_access()
        return self.db.storage.data.get('users', {})