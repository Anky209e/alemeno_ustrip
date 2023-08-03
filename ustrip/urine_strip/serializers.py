from rest_framework import serializers
from .models import UStrip

class UStripSerializer(serializers.ModelSerializer):
    """
    Rest serializer for data serilization
    """
    class Meta:
        model = UStrip

        fields = "__all__"
