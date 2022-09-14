# from urllib import request
# from wsgiref.util import request_uri

# from django.core.exceptions import PermissionDenied
# from django.db.models import Q
# from django.views.decorators import http
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.generics import (
#     CreateAPIView,
#     DestroyAPIView,
#     ListAPIView,
#     UpdateAPIView,
# )
# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet

# from authentication.models import DEFAULT_ROLES
# from core.models import Ticket
# from core.permissions import ClientOnly, OperatorOnly
# from core.serializers import (
#     TicketAssignSerializer,
#     TicketLightSerializer,
#     TicketSerializer,
#     TicketUpdateSerializer,
# )

# #####################################################################


# class TicketsList(ListAPIView):
#     serializer_class = TicketLightSerializer
#     # http_method_names = ["get", "post"]

#     @classmethod
#     @http("GET")
#     def as_view(cls, **initkwargs):

#         return super().as_view()

#     def get_queryset(self):
#         user = self.request.user
#         # params = self.request.query_params
#         if user.role.id == DEFAULT_ROLES["admin"]:
#             return Ticket.objects.filter(Q(operator=None) | Q(operator=user))

#         return Ticket.objects.filter(client=user)


# class TicketsCreate(CreateAPIView):

#     serializer_class = TicketSerializer
#     queryset = Ticket.objects.all()
#     permission_classes = [ClientOnly]

#     @classmethod
#     @http("POST")
#     def as_view(cls, **initkwargs):

#         return super().as_view()


# ######################################################################
# # class TicketsAPIView(ModelViewSet):
# #     def get_queryset(self):
# #         return super().get_queryset()

# #     def create(self, request, *args, **kwargs):
# #         return super().create(request, *args, **kwargs)

# #     def list(self, request, *args, **kwargs):
# #         return super().list(request, *args, **kwargs)

# #     def update(self, request, *args, **kwargs):
# #         return super().update(request, *args, **kwargs)

# #     def destroy(self, request, *args, **kwargs):
# #         return super().destroy(request, *args, **kwargs)
