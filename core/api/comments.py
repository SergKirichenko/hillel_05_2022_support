from rest_framework.generics import CreateAPIView, ListAPIView

from core.models import Comment
from core.serializers import CommentSerializer


class CommentsListAPI(ListAPIView):
    http_method_names = ["get"]
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"
    lookup_url_kwarg = "ticket_id"

    def get_queryset(self):
        ticket_id: int = self.kwargs[self.lookup_field]

        # NOTE: Walrus operator usage
        # if ticket_id := self.kwargs.get(self.lookup_field):
        #     raise ValueError("You can not comment unspecified ticket.")

        return Comment.objects.filter(ticket_id=ticket_id)


class CommentsCreateAPI(CreateAPIView):
    http_method_names = ["post"]
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"
    lookup_url_kwarg = "ticket_id"

    def get_queryset(self):
        ticket_id: int = self.kwargs[self.lookup_field]
        return Comment.objects.filter(ticket_id=ticket_id)
