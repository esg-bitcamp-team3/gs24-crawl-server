# serializers.py
from rest_framework import serializers


class CarbonPriceSerializer(serializers.Serializer):
    basDt = serializers.CharField(max_length=100)
    itmsNm = serializers.CharField(max_length=100)
    clpr = serializers.CharField(max_length=100)
    vs = serializers.CharField(max_length=100)
    fltRt = serializers.CharField(max_length=100)
    trqu = serializers.CharField(max_length=100)
    trPrc = serializers.CharField(max_length=100)

