from .models import AuditLog, Permission, Role, RolePermission, User, UserProfile, UserRole
from .tables import tables
from .schema import SCHEMA_JSON
SCHEMA = {"AuditLog": AuditLog, "Permission": Permission, "Role": Role, "RolePermission": RolePermission, "User": User, "UserProfile": UserProfile, "UserRole": UserRole}
__all__ = ['tables', 'SCHEMA_JSON', 'SCHEMA', 'AuditLog', 'Permission', 'Role', 'RolePermission', 'User', 'UserProfile', 'UserRole']
