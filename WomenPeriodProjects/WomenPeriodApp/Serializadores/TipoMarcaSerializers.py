from rest_framework import serializers
from WomenPeriodApp.models import TipoMarca

class TipoMarcaSerializers(serializers.ModelSerializer):
    class Meta:
        model=TipoMarca
        fields= '__all__'
