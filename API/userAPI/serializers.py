from rest_framework import serializers
from db.models import userDB

class userDBSerializer(serializers.ModelSerializer):
    included_in_these_chats = serializers.JSONField(required=False)

    class Meta:
        model = userDB
        fields = '__all__'