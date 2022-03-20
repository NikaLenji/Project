from classic.http_auth import Group, Permission, strategies


class Permissions:
    FULL_CONTROL = Permission('full_control')


class Groups:
    ADMINS = Group('admins', permissions=(Permissions.FULL_CONTROL, ))


jwt_strategy = strategies.JWT(
    secret_key='this_is_secret_key_for_jwt',
)


ALL_GROUPS = (Groups.ADMINS, )
