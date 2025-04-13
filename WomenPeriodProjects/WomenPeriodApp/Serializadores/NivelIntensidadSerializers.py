from rest_framework import serializers
from WomenPeriodApp.models import NivelIntensidad

class NivelIntensidadSerializers(serializers.ModelSerializer):
    class Meta:
        model=NivelIntensidad
        fields= '__all__'
