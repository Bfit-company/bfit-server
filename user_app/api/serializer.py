from django.contrib.auth import get_user_model
from rest_framework import serializers

from user_app.models import UserDB

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        # overwrite the save method because the pass2 and validate the email

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be the same !'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exist!'})

        account = User(
            email=self.validated_data['email'],
        )
        account.set_password(password)
        account.save()
        return account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDB
        fields = ('id','email')

# #todo: in future
# class LoginSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ['email', 'password']
