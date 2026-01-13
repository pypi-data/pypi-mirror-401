SCHEMA_JSON = {
  "databaseId": "bbabca0e-82ce-11f0-0000-a2ce78b61b6a",
  "revisionDescription": "",
  "entities": [
    {
      "name": "AuditLog",
      "identifier": {
        "name": "id",
        "generator": "None",
        "type": "String"
      },
      "attributes": [
        {
          "name": "action",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "actorId",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "changes",
          "type": "EmbeddedObject",
          "isNullable": True
        },
        {
          "name": "dateTime",
          "type": "Timestamp"
        },
        {
          "name": "errorCode",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "errorMessage",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "id",
          "type": "String"
        },
        {
          "name": "metadata",
          "type": "EmbeddedObject",
          "isNullable": True
        },
        {
          "name": "requestId",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "resource",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "status",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "targetId",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "tenantId",
          "type": "String",
          "isNullable": True
        }
      ]
    },
    {
      "name": "Permission",
      "identifier": {
        "name": "id",
        "generator": "None",
        "type": "String"
      },
      "attributes": [
        {
          "name": "createdAt",
          "type": "Timestamp"
        },
        {
          "name": "deletedAt",
          "type": "Timestamp",
          "isNullable": True
        },
        {
          "name": "description",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "id",
          "type": "String"
        },
        {
          "name": "name",
          "type": "String"
        },
        {
          "name": "updatedAt",
          "type": "Timestamp"
        }
      ]
    },
    {
      "name": "Role",
      "identifier": {
        "name": "id",
        "generator": "None",
        "type": "String"
      },
      "attributes": [
        {
          "name": "createdAt",
          "type": "Timestamp"
        },
        {
          "name": "deletedAt",
          "type": "Timestamp",
          "isNullable": True
        },
        {
          "name": "description",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "id",
          "type": "String"
        },
        {
          "name": "isSystem",
          "type": "Boolean"
        },
        {
          "name": "name",
          "type": "String"
        },
        {
          "name": "updatedAt",
          "type": "Timestamp"
        }
      ],
      "resolvers": [
        {
          "name": "permissions",
          "resolver": "db.from(\"Permission\")\n  .where(\n    inOp(\"id\", \n        db.from(\"RolePermission\")\n            .where(eq(\"roleId\", this.id))\n            .list()\n            .values('permissionId')\n    )\n)\n .list()"
        },
        {
          "name": "rolePermissions",
          "resolver": "db.from(\"RolePermission\")\n .where(eq(\"roleId\", this.id))\n .list()"
        }
      ]
    },
    {
      "name": "RolePermission",
      "identifier": {
        "name": "id",
        "generator": "None",
        "type": "String"
      },
      "attributes": [
        {
          "name": "createdAt",
          "type": "Timestamp"
        },
        {
          "name": "id",
          "type": "String"
        },
        {
          "name": "permissionId",
          "type": "String"
        },
        {
          "name": "roleId",
          "type": "String"
        }
      ],
      "resolvers": [
        {
          "name": "permission",
          "resolver": "db.from(\"Permission\")\n .where(eq(\"id\", this.permissionId))\n .firstOrNull()"
        },
        {
          "name": "role",
          "resolver": "db.from(\"Role\")\n .where(eq(\"id\", this.roleId))\n .firstOrNull()"
        }
      ]
    },
    {
      "name": "User",
      "identifier": {
        "name": "id",
        "generator": "None",
        "type": "String"
      },
      "attributes": [
        {
          "name": "createdAt",
          "type": "Timestamp"
        },
        {
          "name": "deletedAt",
          "type": "Timestamp",
          "isNullable": True
        },
        {
          "name": "email",
          "type": "String"
        },
        {
          "name": "id",
          "type": "String"
        },
        {
          "name": "isActive",
          "type": "Boolean"
        },
        {
          "name": "lastLoginAt",
          "type": "Timestamp",
          "isNullable": True
        },
        {
          "name": "updatedAt",
          "type": "Timestamp"
        },
        {
          "name": "username",
          "type": "String"
        }
      ],
      "resolvers": [
        {
          "name": "profile",
          "resolver": "db.from(\"UserProfile\")\n .where(eq(\"userId\", this.id))\n .firstOrNull()"
        },
        {
          "name": "roles",
          "resolver": "db.from(\"Role\")\n  .where(\n    inOp(\"id\", \n        db.from(\"UserRole\")\n            .where(eq(\"userId\", this.id))\n            .list()\n            .values('roleId')\n    )\n)\n .list()"
        },
        {
          "name": "userRoles",
          "resolver": "db.from(\"UserRole\")\n  .where(eq(\"userId\", this.id))\n  .list()"
        }
      ]
    },
    {
      "name": "UserProfile",
      "identifier": {
        "name": "id",
        "generator": "None",
        "type": "String"
      },
      "attributes": [
        {
          "name": "address",
          "type": "EmbeddedObject",
          "isNullable": True
        },
        {
          "name": "age",
          "type": "Int",
          "isNullable": True
        },
        {
          "name": "avatarUrl",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "bio",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "createdAt",
          "type": "Timestamp"
        },
        {
          "name": "deletedAt",
          "type": "Timestamp",
          "isNullable": True
        },
        {
          "name": "firstName",
          "type": "String"
        },
        {
          "name": "id",
          "type": "String"
        },
        {
          "name": "lastName",
          "type": "String"
        },
        {
          "name": "phone",
          "type": "String",
          "isNullable": True
        },
        {
          "name": "updatedAt",
          "type": "Timestamp",
          "isNullable": True
        },
        {
          "name": "userId",
          "type": "String"
        }
      ]
    },
    {
      "name": "UserRole",
      "identifier": {
        "name": "id",
        "generator": "None",
        "type": "String"
      },
      "attributes": [
        {
          "name": "createdAt",
          "type": "Timestamp"
        },
        {
          "name": "id",
          "type": "String"
        },
        {
          "name": "roleId",
          "type": "String"
        },
        {
          "name": "userId",
          "type": "String"
        }
      ],
      "resolvers": [
        {
          "name": "role",
          "resolver": "db.from(\"Role\")\n .where(eq(\"id\", this.roleId))\n .list()"
        }
      ]
    }
  ]
}
