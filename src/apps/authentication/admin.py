from django.contrib import admin

from apps.authentication.models import Role, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["user_permissions", "groups"]
    readonly_fields = ["password", "last_login"]
    list_display = [
        "id",
        "username",
        "first_name",
        "last_name",
        "age",
        "phone",
        "role",
        "created_at",
        "updated_at",
    ]
    list_filter = ["age"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass
