from rest_framework import serializers
from .models import UStrip

class UStripSerializer(serializers.ModelSerializer):
    class Meta:
        model = UStrip

        fields = "__all__"
