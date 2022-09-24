from django.contrib import admin

from apps.core.models import Comment, Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "theme", "operator", "client", "created_at", "resolved"]
    list_display_links = ["theme"]
    list_filter = ["operator"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "ticket", "user"]
    list_display_links = ["ticket"]
    list_filter = ["ticket"]
