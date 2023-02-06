from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView
from product.models import *
from accounts.models import User


class Userserializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            '__all__'
        )
