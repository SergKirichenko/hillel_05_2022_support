from django.urls import path

from apps.core.api import (
    CommentsCreateAPI,
    CommentsDeleteAPI,
    CommentsListAPI,
    CommentsRepleyToAPI,
    CommentsUpdateAPI,
    TicketAssignAPI,
    TicketResolveAPI,
    TicketRetrieveAPI,
    TicketsDeleteAPI,
    TicketsListCreateAPI,
    TicketsUpdateAPI,
)

tickets_urls = [
    path("", TicketsListCreateAPI.as_view()),
    path("<int:id>/", TicketRetrieveAPI.as_view()),
    path("<int:id>/assign/", TicketAssignAPI.as_view()),
    path("<int:id>/update/", TicketsUpdateAPI.as_view()),
    path("<int:id>/delete/", TicketsDeleteAPI.as_view()),
    path("<int:id>/resolve/", TicketResolveAPI.as_view()),
]

comments_urls = [
    path("<int:ticket_id>/comments/", CommentsListAPI.as_view()),
    path("<int:ticket_id>/comments/create/", CommentsCreateAPI.as_view()),
    path("<int:ticket_id>/comments/<int:comment_id>/repley_to/", CommentsRepleyToAPI.as_view()),
    path("<int:ticket_id>/comments/<int:comment_id>/update/", CommentsUpdateAPI.as_view()),
    path("<int:ticket_id>/comments/<int:comment_id>/delete/", CommentsDeleteAPI.as_view()),
]

urlpatterns = tickets_urls + comments_urls
