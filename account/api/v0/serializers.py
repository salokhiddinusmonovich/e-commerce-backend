from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=100, write_only=True)
    password2 = serializers.CharField(max_length=100, write_only=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError("password is not match password2 ")
        return data

    def create(self, data):
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        user.save()
        return user


class UserUpdateSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'password']



class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password is no match')
        user.set_password(password)
        user.save()
        return attrs


