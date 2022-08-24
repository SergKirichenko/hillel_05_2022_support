from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Ticket
from core.serializers import TicketLightSerializer, TicketSerializer


@api_view(["GET", "POST"])
def get_post_tickets(request):
    if request.method == "GET":
        tickets = Ticket.objects.all()
        data = TicketLightSerializer(tickets, many=True).data
        return Response(data=data)

    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.create(serializer.validated_data)
        results = TicketSerializer(instance).data
        return Response(data=results, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def get_ticket(request, id_: int):
    try:
        ticket = Ticket.objects.get(id=id_)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        data = TicketSerializer(ticket).data
        return Response(data=data)

    elif request.method == "PUT":
        serializer = TicketSerializer(instance=ticket, data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.update(instance=ticket, validated_data=serializer.validated_data)
            result = TicketSerializer(instance).data
            return Response(result, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        ticket.delete()
        message_ = {"message": "Ticket - delete"}
        return Response(message_, status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "DELETE"])
# def delete_ticket(request, id_: int):
#     try:
#         Ticket.objects.get(id=id_).delete()
#         message_ = {"message": "Ticket - delete"}
#         return Response(message_, status=status.HTTP_204_NO_CONTENT)
#     except Ticket.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
