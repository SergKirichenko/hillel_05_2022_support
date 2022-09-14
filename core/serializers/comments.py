from typing import TypeVar

from rest_framework import serializers

from core.models import Comment, Ticket

COMMENT_TYPE = TypeVar("COMMENT_TYPE", Comment, None)


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    prev_comment = serializers.IntegerField(read_only=True, allow_null=True)
    # ticket = serializers.PrimaryKeyRelatedField(read_only=True)
    # user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["ticket", "user", "prev_comment"]

    def validate(self, attrs: dict) -> dict:
        request = self.context["request"]
        ticket_id: int = request.parser_context["kwargs"]["ticket_id"]
        ticket: Ticket = Ticket.objects.get(id=ticket_id)

        attrs["ticket"] = ticket
        attrs["user"] = request.user

        last_comment: COMMENT_TYPE = ticket.comments.last()

        attrs["prev_comment"] = last_comment if last_comment else None

        return attrs

    def create(self, validated_data):
        instance = Comment.objects.create(**validated_data)
        return instance
