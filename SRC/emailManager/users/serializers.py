from rest_framework import serializers


class ContactUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    birthdate = serializers.DateField()


class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    body = serializers.CharField()
    author = serializers.CharField()
    created_date = serializers.DateTimeField()
