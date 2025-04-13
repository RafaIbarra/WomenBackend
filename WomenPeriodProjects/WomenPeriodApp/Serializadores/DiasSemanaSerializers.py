from rest_framework import serializers
from WomenPeriodApp.models import DiasSemana

class DiasSemanaSerializers(serializers.ModelSerializer):
    class Meta:
        model=DiasSemana
        fields= '__all__'
