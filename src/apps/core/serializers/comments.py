from typing import TypeVar

from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.core.models import Comment, Ticket

COMMENT_TYPE = TypeVar("COMMENT_TYPE", Comment, None)


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["ticket", "user", "prev_comment"]

    def validate(self, attrs: dict) -> dict:

        ticket, request, attrs = validate_ticket_on_operator_and_resolved(self, attrs)
        last_comment: COMMENT_TYPE = ticket.comments.last()

        attrs["ticket"] = ticket
        attrs["user"] = request.user
        attrs["prev_comment"] = last_comment if last_comment else None

        return attrs

    def create(self, validated_data):
        instance = Comment.objects.create(**validated_data)
        return instance


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentRepleyToSerializer(serializers.ModelSerializer):
    text = serializers.CharField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["ticket", "user", "prev_comment"]

    def validate(self, attrs: dict) -> dict:
        ticket, request, attrs = validate_ticket_on_operator_and_resolved(self, attrs)
        last_comment: COMMENT_TYPE = ticket.comments.last()

        comment_id: int = request.parser_context["kwargs"]["comment_id"]
        reply_to_comment: Comment = Comment.objects.get(id=comment_id)

        attrs["reply_to"] = reply_to_comment
        attrs["ticket"] = ticket
        attrs["user"] = request.user
        attrs["prev_comment"] = last_comment if last_comment else None

        return attrs


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text"]

    def validate(self, attrs):
        validate_ticket_on_operator_and_resolved(self, attrs)
        return attrs


def validate_ticket_on_operator_and_resolved(self, attrs):
    request = self.context["request"]
    ticket_id: int = request.parser_context["kwargs"]["ticket_id"]
    ticket: Ticket = Ticket.objects.get(id=ticket_id)

    # NOTE: Can't recomment if ticket is resolved
    resolve: Ticket = ticket.resolved
    if resolve is True:
        raise ValidationError("Problem solved. Comments on the ticket are closed.")

    # NOTE: Can't comment if ticket is resolved
    resolve: Ticket = ticket.resolved
    if resolve is True:
        raise ValidationError("Problem solved. Comments on the ticket are closed.")

    return ticket, request, attrs
