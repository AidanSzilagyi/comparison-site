from enum import Enum
from .models import List

class AccessLevel(Enum):
    VIEW = 1
    RANK = 2
    EDIT = 3

class Policy(Enum):
    OWNER = 1
    INVITED = 2
    ANYONE = 3
    
ACCESS_MATRIX = {
    List.Permission.PRIVATE: {
        AccessLevel.VIEW: Policy.OWNER,
        AccessLevel.RANK: Policy.OWNER,
        AccessLevel.EDIT: Policy.OWNER,
    },
    List.Permission.PROTECTED: {
        AccessLevel.VIEW: Policy.ANYONE,
        AccessLevel.RANK: Policy.OWNER,
        AccessLevel.EDIT: Policy.OWNER,
    },
    List.Permission.INVITE_RANK: {
        AccessLevel.VIEW: Policy.ANYONE,
        AccessLevel.RANK: Policy.INVITED,
        AccessLevel.EDIT: Policy.OWNER,
    },
    List.Permission.INVITE_VIEW: {
        AccessLevel.VIEW: Policy.INVITED,
        AccessLevel.RANK: Policy.INVITED,
        AccessLevel.EDIT: Policy.OWNER,
    },
    List.Permission.PUBLIC: {
        AccessLevel.VIEW: Policy.ANYONE,
        AccessLevel.RANK: Policy.ANYONE,
        AccessLevel.EDIT: Policy.OWNER,
    },
}

def permission_check(user, tlist: List, access_level: AccessLevel):
    policy = ACCESS_MATRIX[List.Permission(tlist.permission)][access_level]
    if not user.is_authenticated:
        return access_level == AccessLevel.VIEW and policy == Policy.ANYONE
    
    match policy:
        case Policy.ANYONE:
            return True
        case Policy.OWNER:
            return user == tlist.user
        case Policy.INVITED:
            return user == tlist.user or tlist.permitted_users.filter(pk=user.pk).exists()
    return False
            