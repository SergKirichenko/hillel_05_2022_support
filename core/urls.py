from django.urls import path

from core.api import get_post_tickets, get_put_del_ticket

urlpatterns = [
    path("", get_post_tickets),
    path("<int:id_>/", get_put_del_ticket),
]
