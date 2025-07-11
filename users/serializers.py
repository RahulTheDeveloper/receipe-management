from rest_framework import serializers
from .models import CustomUser, CreatorProfile, ViewerProfile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_type = validated_data.get('user_type')

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        if user_type == 'creator':
            CreatorProfile.objects.create(user=user)
        elif user_type == 'viewer':
            ViewerProfile.objects.create(user=user)

        return user
