from django.urls import path

from core.api import (
    TicketAssignAPI,
    TicketRetrieveAPI,
    TicketsDeleteAPI,
    TicketsListCreateAPI,
    TicketsUpdateAPI,
)

urlpatterns = [
    path("", TicketsListCreateAPI.as_view()),
    path("<int:id>/", TicketRetrieveAPI.as_view()),
    path("<int:id>/assign/", TicketAssignAPI.as_view()),
    path("<int:id>/update/", TicketsUpdateAPI.as_view()),
    path("<int:id>/delete/", TicketsDeleteAPI.as_view()),
]

# path("", TicketsListAPI.as_view()),
# path("", TicketsCreateAPI.as_view()),
# path("<int:id>/rud/", TicketRUDAPI.as_view()),
##################################################################
