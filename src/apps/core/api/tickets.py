from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response

from apps.authentication.models import DEFAULT_ROLES
from apps.core.models import Ticket
from apps.core.permissions import ClientOnly, OperatorOnly, PermissionTicketDelete
from apps.core.serializers import (
    TicketAssignSerializer,
    TicketLightSerializer,
    TicketSerializer,
    TicketUpdateSerializer,
)
from apps.core.services import TicketsCRUD


# '''GET, POST'''
class TicketsListCreateAPI(ListCreateAPIView):
    serializer_class = TicketSerializer
    permission = ClientOnly

    def get_queryset(self):
        # NOTE: Filtering tickets according params

        user = self.request.user

        if user.role.id == DEFAULT_ROLES["admin"]:
            empty = self.request.query_params["empty"]
            if empty == "True":
                return Ticket.objects.filter(operator=None)
            elif empty == "False":
                return Ticket.objects.filter(Q(operator=None) | Q(operator=user))
            raise ValidationError
        if user.role.id == DEFAULT_ROLES["user"]:
            return Ticket.objects.filter(client=user)

    # '''GET'''
    def list(self, request, *args, **kwargs):
        # NOTE: Get all user Ticket:
        #      - If User = Role-user, he get his own tickets;
        #      - If User = Role-admin, he get his own tickets(where he is signed like - operator),
        #        and  tickets without operator.

        queryset = self.get_queryset()
        serializer = TicketLightSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # '''POST'''
    def create(self, request, *args, **kwargs):
        # NOTE: If User Role=admin, you can't create the ticket

        if self.permission.has_permission(self, request=request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise PermissionDenied


# '''GET '''
class TicketRetrieveAPI(RetrieveAPIView):
    # NOTE: View one ticket

    serializer_class = TicketSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        if user.role.id == DEFAULT_ROLES["user"]:
            return Ticket.objects.filter(client=user)
        return Ticket.objects.filter(operator=user)


# '''PATCH'''
class TicketAssignAPI(UpdateAPIView):
    # NOTE: If User_role=admin, he assign "no-operator" ticket for self

    http_method_names = ["patch"]
    serializer_class = TicketAssignSerializer
    permission_classes = [OperatorOnly]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Ticket.objects.filter(operator=None)


# '''PATCH'''
class TicketResolveAPI(UpdateAPIView):
    # NOTE: Doing the change in Resolved mark

    http_method_names = ["patch"]
    permission_classes = [OperatorOnly]
    serializer_class = TicketLightSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(operator=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = TicketsCRUD.change_resolved_status(instance)

        # serializer = self.serializer_class(instance)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


# '''PUT, PATCH'''
class TicketsUpdateAPI(UpdateAPIView):
    # NOTE: Only client can update own tickets, in two fields (theme, discription)

    serializer_class = TicketUpdateSerializer
    permission_classes = [ClientOnly]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(client=user)


# '''DELETE'''
class TicketsDeleteAPI(RetrieveDestroyAPIView):
    # NOTE: Allow delete on specific procedure (description in permissions.py)
    serializer_class = TicketSerializer
    permission_classes = [PermissionTicketDelete]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(Q(operator=user) | Q(client=user))
        # return Ticket.objects.filter(Q(operator=user) & Q(reversed=True))
