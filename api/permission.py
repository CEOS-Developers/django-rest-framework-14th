from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsAuthorOrReadonly(permissions.BasePermission):
    # 인증된 유저에 대해 조회/포스팅 허용.
    def has_permission(self, request, view):
        return request.user.is_authenticated
    # 작성자는 삭제 허용
    def has_object_permission(self, request, view, obj):
        # 안전한 요청은 항상 허용.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_superuser)

class AuthorOnly(permissions.BasePermission):
    # 조회는 되나? 조회 막을 방법이 없나.
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        # 작성자만 허용.
        return obj.author == request.user