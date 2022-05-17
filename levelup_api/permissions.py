from rest_framework.permissions import BasePermission


class IsSystemAdminUser(BasePermission):
    def has_permission(self, req, view):
        return bool(req.user and req.user.is_system_admin)


class IsStudentUser(BasePermission):
    def has_permission(self, req, view):
        return bool(req.user and req.user.is_student)


class IsTeacherUser(BasePermission):
    def has_permission(self, req, view):
        return bool(req.user and req.user.is_teacher)


class IsLanguageNativeUser(BasePermission):
    def has_permission(self, req, view):
        return bool(req.user and req.user.is_language_native)
