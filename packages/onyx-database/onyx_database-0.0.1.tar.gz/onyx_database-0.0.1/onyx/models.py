import datetime
from typing import Any, Optional

class AuditLog:
    """Generated model (plain Python class). Resolver/extra fields are allowed via **extra."""
    def __init__(self, action: Optional[str] = None, actorId: Optional[str] = None, changes: Optional[dict] = None, dateTime: datetime.datetime = None, errorCode: Optional[str] = None, errorMessage: Optional[str] = None, id: str = None, metadata: Optional[dict] = None, requestId: Optional[str] = None, resource: Optional[str] = None, status: Optional[str] = None, targetId: Optional[str] = None, tenantId: Optional[str] = None, **extra: Any):
        self.action = action
        self.actorId = actorId
        self.changes = changes
        self.dateTime = dateTime
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.id = id
        self.metadata = metadata
        self.requestId = requestId
        self.resource = resource
        self.status = status
        self.targetId = targetId
        self.tenantId = tenantId
        # allow resolver-attached fields or extra properties
        for k, v in extra.items():
            setattr(self, k, v)


class Permission:
    """Generated model (plain Python class). Resolver/extra fields are allowed via **extra."""
    def __init__(self, createdAt: datetime.datetime = None, deletedAt: Optional[datetime.datetime] = None, description: Optional[str] = None, id: str = None, name: str = None, updatedAt: datetime.datetime = None, **extra: Any):
        self.createdAt = createdAt
        self.deletedAt = deletedAt
        self.description = description
        self.id = id
        self.name = name
        self.updatedAt = updatedAt
        # allow resolver-attached fields or extra properties
        for k, v in extra.items():
            setattr(self, k, v)


class Role:
    """Generated model (plain Python class). Resolver/extra fields are allowed via **extra."""
    def __init__(self, createdAt: datetime.datetime = None, deletedAt: Optional[datetime.datetime] = None, description: Optional[str] = None, id: str = None, isSystem: bool = None, name: str = None, updatedAt: datetime.datetime = None, **extra: Any):
        self.createdAt = createdAt
        self.deletedAt = deletedAt
        self.description = description
        self.id = id
        self.isSystem = isSystem
        self.name = name
        self.updatedAt = updatedAt
        # allow resolver-attached fields or extra properties
        for k, v in extra.items():
            setattr(self, k, v)


class RolePermission:
    """Generated model (plain Python class). Resolver/extra fields are allowed via **extra."""
    def __init__(self, createdAt: datetime.datetime = None, id: str = None, permissionId: str = None, roleId: str = None, **extra: Any):
        self.createdAt = createdAt
        self.id = id
        self.permissionId = permissionId
        self.roleId = roleId
        # allow resolver-attached fields or extra properties
        for k, v in extra.items():
            setattr(self, k, v)


class User:
    """Generated model (plain Python class). Resolver/extra fields are allowed via **extra."""
    def __init__(self, createdAt: datetime.datetime = None, deletedAt: Optional[datetime.datetime] = None, email: str = None, id: str = None, isActive: bool = None, lastLoginAt: Optional[datetime.datetime] = None, updatedAt: datetime.datetime = None, username: str = None, **extra: Any):
        self.createdAt = createdAt
        self.deletedAt = deletedAt
        self.email = email
        self.id = id
        self.isActive = isActive
        self.lastLoginAt = lastLoginAt
        self.updatedAt = updatedAt
        self.username = username
        # allow resolver-attached fields or extra properties
        for k, v in extra.items():
            setattr(self, k, v)


class UserProfile:
    """Generated model (plain Python class). Resolver/extra fields are allowed via **extra."""
    def __init__(self, address: Optional[dict] = None, age: Optional[int] = None, avatarUrl: Optional[str] = None, bio: Optional[str] = None, createdAt: datetime.datetime = None, deletedAt: Optional[datetime.datetime] = None, firstName: str = None, id: str = None, lastName: str = None, phone: Optional[str] = None, updatedAt: Optional[datetime.datetime] = None, userId: str = None, **extra: Any):
        self.address = address
        self.age = age
        self.avatarUrl = avatarUrl
        self.bio = bio
        self.createdAt = createdAt
        self.deletedAt = deletedAt
        self.firstName = firstName
        self.id = id
        self.lastName = lastName
        self.phone = phone
        self.updatedAt = updatedAt
        self.userId = userId
        # allow resolver-attached fields or extra properties
        for k, v in extra.items():
            setattr(self, k, v)


class UserRole:
    """Generated model (plain Python class). Resolver/extra fields are allowed via **extra."""
    def __init__(self, createdAt: datetime.datetime = None, id: str = None, roleId: str = None, userId: str = None, **extra: Any):
        self.createdAt = createdAt
        self.id = id
        self.roleId = roleId
        self.userId = userId
        # allow resolver-attached fields or extra properties
        for k, v in extra.items():
            setattr(self, k, v)

