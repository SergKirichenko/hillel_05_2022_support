from django.contrib import admin

from .models import Comment, Ticket

# @admin.site.register(User)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "theme", "operator", "client", "created_at"]
    list_display_links = ["theme"]
    list_filter = ["operator"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "ticket"]
    list_display_links = ["ticket"]
    list_filter = ["ticket"]
