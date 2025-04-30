from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TodoModel

# register serializer
# This serializer is used to validate and create a new user.
class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_password(self , password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return password
    
    def create(self , validated_data):
        user = User.objects.create(
            first_name =validated_data['first_name'],
            last_name =validated_data['last_name'],
            username =validated_data['username'],
            email =validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


# login serializer
# This serializer is used to validate the user credentials during login.
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModel
        fields = ['id', 'title', 'description', 'user', 'is_completed', 'created_at', 'updated_at']
        read_only_fields = ['user', 'is_completed', 'created_at', 'updated_at']
        

    def validate(self, data):
        if len(data.get('title', '')) < 1:
            raise serializers.ValidationError("Title must be at least 1 character long.")
        if len(data.get('description', '')) < 1:
            raise serializers.ValidationError("Description must be at least 1 character long.")
        return data

    def create(self, validated_data):
        # user is not in validated_data because it's read-only; we add it manually
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
