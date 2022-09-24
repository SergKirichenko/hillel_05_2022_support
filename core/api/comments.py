from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
)

from core.models import Comment
from core.permissions import OwnerCommentPermissions, OwnerTicketPermissions
from core.serializers import (
    CommentRepleyToSerializer,
    CommentSerializer,
    CommentsListSerializer,
    CommentUpdateSerializer,
)


class CommentsListAPI(ListAPIView):
    # NOTE: View all comments list
    http_method_names = ["get"]
    permission_classes = [OwnerTicketPermissions]
    serializer_class = CommentsListSerializer
    lookup_field = "ticket_id"
    lookup_url_kwarg = "ticket_id"

    def get_queryset(self):
        ticket_id: int = self.kwargs[self.lookup_field]

        # NOTE: Walrus operator usage
        # if ticket_id := self.kwargs.get(self.lookup_field):
        #     raise ValueError("You can not comment unspecified ticket.")

        return Comment.objects.filter(ticket_id=ticket_id)


class CommentsCreateAPI(CreateAPIView):
    # NOTE: Create comment if validation terms is well
    http_method_names = ["post"]
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"

    def get_queryset(self):
        ticket_id: int = self.kwargs[self.lookup_field]
        return Comment.objects.filter(ticket_id=ticket_id)


class CommentsRepleyToAPI(CreateAPIView):
    # NOTE: You can repley to other comments in this ticket-list
    http_method_names = ["post"]
    serializer_class = CommentRepleyToSerializer


class CommentsUpdateAPI(UpdateAPIView):
    # NOTE: Update own comment
    http_method_names = ["put", "patch"]
    permission_classes = [OwnerCommentPermissions]
    serializer_class = CommentUpdateSerializer
    lookup_field = "ticket_id"

    def get_queryset(self):
        comment_id = self.kwargs["comment_id"]
        return Comment.objects.filter(id=comment_id)


class CommentsDeleteAPI(DestroyAPIView):
    # NOTE: Delete own comment
    http_method_names = ["delete"]
    permission_classes = [OwnerCommentPermissions]
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"

    def get_queryset(self):
        comment_id = self.kwargs["comment_id"]
        return Comment.objects.filter(id=comment_id)
