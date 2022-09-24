from itertools import chain

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.authentication.models import Role
from apps.core.models import Ticket

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = [
            "created_at",
            "updated_at",
        ]


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        exclude = [
            "password",
            "last_login",
            "updated_at",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
            "updateed_at",
            "groups",
            "user_permissions",
        ]


class TicketSerializer(serializers.ModelSerializer):
    operator = UserSerializer(read_only=True)
    client = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"

    def validate(self, attrs: dict) -> dict:
        theme = attrs.get("theme")
        if not theme:
            return attrs

        data = Ticket.objects.values_list("theme")
        for element in chain.from_iterable(data):
            if element == theme:
                raise ValidationError("This ticket is already in database")

        attrs["client"] = self.context["request"].user
        return attrs


class TicketLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "theme", "resolved", "operator", "client"]


class TicketAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["operator"]

    def validate(self, attrs: dict) -> dict:
        # NOTE: Add current user to the `attrs` object
        attrs["operator"] = self.context["request"].user
        return attrs


class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["theme", "description", "updated_at"]
