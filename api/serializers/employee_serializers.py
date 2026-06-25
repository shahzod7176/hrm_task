from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.employees.models import Employee



class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
    )
    password2 = serializers.CharField(
        write_only=True, required=True,
        label='Подтверждение пароля',
        style={'input_type': 'password'},
    )

    class Meta:
        model  = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'email':      {'required': True},
            'first_name': {'required': False},
            'last_name':  {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    access  = serializers.CharField(help_text='Access token (1 час)')
    refresh = serializers.CharField(help_text='Refresh token (7 дней)')


class RegisterResponseSerializer(serializers.Serializer):
    user    = serializers.DictField(help_text='Данные пользователя')
    access  = serializers.CharField()
    refresh = serializers.CharField()



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model        = Employee
        fields       = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_phone(self, value):
        value = value.strip()
        if not value.startswith('+'):
            raise serializers.ValidationError('Телефон должен начинаться с "+".')
        return value


class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Employee
        fields = ('id', 'full_name', 'phone', 'email', 'position', 'salary', 'hired_date')
