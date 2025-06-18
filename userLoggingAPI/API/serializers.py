from rest_framework import serializers
from db.models import dbModel

class dbModelSerializer(serializers.ModelSerializer):
    included_in_these_chats = serializers.JSONField(required=False)

    class Meta:
        model = dbModel
        fields = '__all__'