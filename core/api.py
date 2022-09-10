from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response

from authentication.models import DEFAULT_ROLES
from core.models import Ticket
from core.permissions import ClientOnly, OperatorOnly, PermissionTicketDelete
from core.serializers import (
    TicketAssignSerializer,
    TicketLightSerializer,
    TicketSerializer,
    TicketUpdateSerializer,
)


class TicketsListCreateAPI(ListCreateAPIView):
    serializer_class = TicketSerializer
    permission = ClientOnly

    def get_queryset(self):
        user = self.request.user
        if user.role.id == DEFAULT_ROLES["admin"]:
            return Ticket.objects.filter(Q(operator=None) | Q(operator=user))

        return Ticket.objects.filter(client=user)

    @action(methods="GET", detail=False)
    def list(self, request, *args, **kwargs):
        #    Get all user Ticket:
        #     - If User = Role - user, he get his own tickets;
        #     - If User = Role - admin, he get his own tickets(where he is signed like - operator),
        #     and  tickets without operator.
        queryset = self.get_queryset()
        serializer = TicketLightSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods="POST", detail=False)
    def create(self, request, *args, **kwargs):
        #  User - Role = admin can't create the ticket

        if self.permission.has_permission(self, request=request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        raise PermissionDenied


# '''GET (one ticket)'''
class TicketRetrieveAPI(RetrieveAPIView):
    serializer_class = TicketSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        if user.role.id == DEFAULT_ROLES["user"]:
            return Ticket.objects.filter(client=user)
        return Ticket.objects.filter(operator=user)


# ''' PATCH'''
class TicketAssignAPI(UpdateAPIView):
    """if User = role - admin, he assign "no-operator" ticket for self"""

    http_method_names = ["patch"]
    serializer_class = TicketAssignSerializer
    permission_classes = [OperatorOnly]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Ticket.objects.filter(operator=None)


# '''Update - PUT, PATCH'''
class TicketsUpdateAPI(UpdateAPIView):

    serializer_class = TicketUpdateSerializer
    permission_classes = [ClientOnly]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(client=user)


# '''DELETE'''
class TicketsDeleteAPI(RetrieveDestroyAPIView):
    # Allow delete on specific procedure
    serializer_class = TicketSerializer
    permission_classes = [PermissionTicketDelete]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(Q(operator=user) | Q(client=user))
        # return Ticket.objects.filter(Q(operator=user) & Q(reversed=True))


####################################################################################################
# Ниже нужно дорабатываь №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№
# class TicketRUDAPI(RetrieveUpdateDestroyAPIView):
#     serializer_class = TicketSerializer
#     lookup_field = "id"
#     lookup_url_kwarg = "id"
#     permission_classes = [ClientOnly, OperatorOnly]

#     def get_queryset(self):
#         return Ticket.objects.filter(client=self.request.user)

#     @action(methods="DELETE", detail=True)
#     def destroy(self, request, *args, **kwargs):
#         permission_classes = OperatorOnly
#         if permission_classes is True:
#             instance = self.get_queryset()
#             instance.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         raise PermissionDenied

# @action(methods="DELET", detail=True)
# def destroy(self, request, *args, **kwargs):
#     filter_kwargs = {self.lookup_field: self.lookup_url_kwarg}
#     instance = self.get_object_or_404(self.get_queryset(), **filter_kwargs)
#     instance.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# '''GET'''######################################################################################
# class TicketsListAPI(ListAPIView):

#     serializer_class = TicketLightSerializer
#     def get_queryset(self):
#         user = self.request.user
#         if user.role.id == DEFAULT_ROLES["admin"]:
#             return Ticket.objects.filter(Q(operator=None) | Q(operator=user))

#         return Ticket.objects.filter(client=user)
# # '''POST'''
# class TicketsCreateAPI(CreateAPIView):

#     serializer_class = TicketSerializer
#     queryset = Ticket.objects.all()
#     permission_classes = [ClientOnly]

####################################################################################################

# class TicketsListCreateAPI(ListCreateAPIView):
#     serializer_class = TicketSerializer
#     queryset = Ticket.objects.all()

#     def get_permissions(self):
#         if self.request.method == "POST":
#             return [IsAuthenticated()]
#         return []

#     def get_serializer(self, *args, **kwargs):
#         return TicketLightSerializer if self.request.method == "GET" else TicketSerializer


# class TicketUpdateAPI(UpdateAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     lookup_field = "id"
#     lookup_url_kwarg = "id"

# class TicketDeleteAPI(DestroyAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     lookup_field = "id"
#     lookup_url_kwarg = "id"


#############################################################################
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.response import Response

# from core.models import Ticket
# from core.serializers import TicketLightSerializer, TicketSerializer

# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def get_post_tickets(request):
#     """
#     GET all visitors can take to watch all tickets in a list , POST ticket can do only authenticated users.
#     """
#     if request.method == "GET":
#         tickets = Ticket.objects.all()
#         data: dict = TicketLightSerializer(tickets, many=True).data
#         return Response(data=data)

#     serializer = TicketSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         instance: Ticket = serializer.create(serializer.validated_data)
#         results: dict = TicketSerializer(instance).data
#         return Response(data=results, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET", "PUT", "DELETE"])
# @permission_classes([IsAuthenticated])
# def get_put_del_ticket(request, id_: int):
#     """
#     These functions can do only authenticated users:
#     GET - detal view one ticket.
#     PUT - update data in ticket("theme", "description", "resolved"(only admin)-(doesn't do yet))
#     DELETE - will delete chosen ticket.
#     """
#     try:
#         ticket = Ticket.objects.get(id=id_)
#     except Ticket.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         data: dict = TicketSerializer(ticket).data
#         return Response(data=data)

#     elif request.method == "PUT":
#         serializer = TicketSerializer(instance=ticket, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             instance: Ticket = serializer.update(instance=ticket, validated_data=serializer.validated_data)
#             result: dict = TicketSerializer(instance).data
#             return Response(result, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == "DELETE":
#         ticket.delete()
#         message_ = {"message": "Ticket - delete"}
#         return Response(message_, status=status.HTTP_204_NO_CONTENT)
