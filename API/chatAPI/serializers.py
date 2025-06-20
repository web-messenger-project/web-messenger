from rest_framework import serializers
from db.models import chatDB

class chatDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = chatDB
        fields = '__all__'