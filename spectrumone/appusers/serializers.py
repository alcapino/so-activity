from rest_framework import serializers
from appusers.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'firstname', 'lastname', 'active', 'activation_token')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.active = validated_data.get('active', instance.active)
        instance.activation_token = validated_data.get('activation_token', instance.activation_token)
        instance.save()
        return instance