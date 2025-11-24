class ServiceExceptions:
    class UserNotFound(Exception):
        pass

    class GroupNotFound(Exception):
        pass

    class NasNotFound(Exception):
        pass

    class UserAlreadyExists(Exception):
        pass

    class GroupAlreadyExists(Exception):
        pass

    class NasAlreadyExists(Exception):
        pass

    class UserWouldBeDeleted(Exception):
        pass

    class GroupWouldBeDeleted(Exception):
        pass

    class GroupStillHasUsers(Exception):
        pass

    class HuntGroupNotFound(Exception):
        pass
