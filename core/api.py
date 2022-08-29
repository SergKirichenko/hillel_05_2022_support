from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.models import Ticket
from core.serializers import TicketLightSerializer, TicketSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_post_tickets(request):
    """
    GET all visitors can take to watch all tickets in a list , POST ticket can do only authenticated users.
    """
    if request.method == "GET":
        tickets = Ticket.objects.all()
        data: dict = TicketLightSerializer(tickets, many=True).data
        return Response(data=data)

    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance: Ticket = serializer.create(serializer.validated_data)
        results: dict = TicketSerializer(instance).data
        return Response(data=results, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def get_put_del_ticket(request, id_: int):
    """
    These functions can do only authenticated users:
    GET - detal view one ticket.
    PUT - update data in ticket("theme", "description", "resolved"(only admin)-(doesn't do yet))
    DELETE - will delete chosen ticket.
    """
    try:
        ticket = Ticket.objects.get(id=id_)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        data: dict = TicketSerializer(ticket).data
        return Response(data=data)

    elif request.method == "PUT":
        serializer = TicketSerializer(instance=ticket, data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance: Ticket = serializer.update(instance=ticket, validated_data=serializer.validated_data)
            result: dict = TicketSerializer(instance).data
            return Response(result, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        ticket.delete()
        message_ = {"message": "Ticket - delete"}
        return Response(message_, status=status.HTTP_204_NO_CONTENT)


# #########################################################################################
# @api_view(["GET", "DELETE"])
# def delete_ticket(request, id_: int):
#     try:
#         Ticket.objects.get(id=id_).delete()
#         message_ = {"message": "Ticket - delete"}
#         return Response(message_, status=status.HTTP_204_NO_CONTENT)
#     except Ticket.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
