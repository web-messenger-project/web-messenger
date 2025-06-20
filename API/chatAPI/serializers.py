from rest_framework import serializers
from db.models import chatDB

class chatDBSerializer(serializers.ModelSerializer):
    messages = serializers.JSONField(required=False)

    class Meta:
        model = chatDB
        fields = '__all__'

class chatDBMessagesSerializer(serializers.ModelSerializer):
    messages = serializers.JSONField(required=True)

    class Meta:
        model = chatDB
        fields = ['messages']

class chatDBMembersSerializer(serializers.ModelSerializer):
    members = serializers.JSONField(required=True)

    class Meta:
        model = chatDB
        fields = ['members']