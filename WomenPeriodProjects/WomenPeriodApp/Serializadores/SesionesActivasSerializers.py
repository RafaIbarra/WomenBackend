from rest_framework import serializers
from WomenPeriodApp.models import SesionesActivas
class SesionesActivasSerializers(serializers.ModelSerializer):
    class Meta:
        model=SesionesActivas
        fields= '__all__'