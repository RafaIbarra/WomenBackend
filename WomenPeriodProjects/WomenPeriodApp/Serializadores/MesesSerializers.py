from rest_framework import serializers
from WomenPeriodApp.models import Meses

class MesesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Meses
        fields= '__all__'
