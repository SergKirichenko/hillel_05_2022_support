from django.urls import path

from core.api import (
    CommentsCreateAPI,
    CommentsListAPI,
    TicketAssignAPI,
    TicketResolveAPI,
    TicketRetrieveAPI,
    TicketsDeleteAPI,
    TicketsListCreateAPI,
    TicketsUpdateAPI,
)

# from core.tickets import TicketsCreate, TicketsList

tickets_urls = [
    path("", TicketsListCreateAPI.as_view()),
    path("<int:id>/", TicketRetrieveAPI.as_view()),
    path("<int:id>/assign/", TicketAssignAPI.as_view()),
    path("<int:id>/update/", TicketsUpdateAPI.as_view()),
    path("<int:id>/delete/", TicketsDeleteAPI.as_view()),
    path("<int:id>/resolve/", TicketResolveAPI.as_view()),
    # path("", TicketsList.as_view()),
    # path("", TicketsCreate.as_view()),
]

comments_urls = [
    path("<int:ticket_id>/comments/", CommentsListAPI.as_view()),
    path("<int:ticket_id>/comments/create/", CommentsCreateAPI.as_view()),
]

urlpatterns = tickets_urls + comments_urls

# path("", TicketsListAPI.as_view()),
# path("", TicketsCreateAPI.as_view()),
# path("<int:id>/rud/", TicketRUDAPI.as_view()),
##################################################################
