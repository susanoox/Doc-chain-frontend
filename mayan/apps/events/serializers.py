from django.utils.translation import gettext_lazy as _

from actstream.models import Action
from rest_framework.reverse import reverse

from mayan.apps.common.serializers import ContentTypeSerializer
from mayan.apps.rest_api import serializers
from mayan.apps.rest_api.fields import DynamicSerializerField
from mayan.apps.user_management.serializers import UserSerializer

from .classes import EventType
from .models import Notification, StoredEventType


class EventTypeNamespaceSerializer(serializers.Serializer):
    event_types_url = serializers.HyperlinkedIdentityField(
        lookup_field='name',
        view_name='rest_api:event-type-namespace-event-type-list'
    )
    label = serializers.CharField(
        label=_(message='Label')
    )
    name = serializers.CharField(
        label=_(message='Name')
    )
    url = serializers.SerializerMethodField(
        label=_(message='URL')
    )

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:event-type-namespace-detail', kwargs={
                'name': instance.name
            }, request=self.context['request'], format=self.context['format']
        )


class EventTypeSerializer(serializers.Serializer):
    event_type_namespace_url = serializers.SerializerMethodField(
        label=_(message='Event type namespace URL')
    )
    id = serializers.CharField(
        label=_(message='ID')
    )
    label = serializers.CharField(
        label=_(message='Label')
    )
    name = serializers.CharField(
        label=_(message='Name')
    )

    def get_event_type_namespace_url(self, instance):
        return reverse(
            viewname='rest_api:event-type-namespace-detail', kwargs={
                'name': instance.namespace.name
            }, request=self.context['request'], format=self.context['format']
        )

    def to_representation(self, instance):
        if isinstance(instance, EventType):
            return super().to_representation(instance=instance)
        elif isinstance(instance, StoredEventType):
            return super().to_representation(instance=instance.event_type)
        elif isinstance(instance, str):
            return super().to_representation(
                instance=EventType.get(id=instance)
            )


class EventSerializer(serializers.ModelSerializer):
    actor = DynamicSerializerField(
        label=_(message='Actor'), read_only=True
    )
    actor_content_type = ContentTypeSerializer(
        label=_(message='Actor content type'), read_only=True
    )
    target = DynamicSerializerField(
        label=_(message='Target'), read_only=True
    )
    target_content_type = ContentTypeSerializer(
        label=_(message='Target content type'), read_only=True
    )
    verb = EventTypeSerializer(
        label=_(message='Verb'), read_only=True
    )

    class Meta:
        exclude = (
            'action_object_content_type', 'action_object_object_id'
        )
        model = Action
        read_only_fields = (
            'action', 'actor_content_type', 'target', 'target_content_type',
            'verb'
        )


class NotificationSerializer(serializers.ModelSerializer):
    action = EventSerializer(
        label=_(message='Action'), read_only=True
    )
    user = UserSerializer(
        label=_(message='User'), read_only=True
    )

    class Meta:
        fields = ('action', 'read', 'user')
        model = Notification
        read_only_fields = ('action', 'user')
