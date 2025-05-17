from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

# ✅ Serializes User Data for API Responses
class UserSerializer(serializers.ModelSerializer):
    """ Provides safe user data for API responses """
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']  # Prevents modifying ID field


# ✅ Handles User Registration with Comprehensive Validation
class RegisterSerializer(serializers.ModelSerializer):
    """ 
    - Includes password strength validation
    - Ensures email/username uniqueness
    - Normalizes input data
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]  # ✅ Uses Django's built-in validation
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'min_length': 4}
        }

    def validate_username(self, value):
        """ Normalizes and validates username """
        value = value.lower().strip()
        if not value.isalnum():
            raise serializers.ValidationError("Username must be alphanumeric")
        if CustomUser.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        """ Normalizes and validates email """
        value = value.lower().strip()
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, attrs):
        """ Cross-field validation to ensure password confirmation matches """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        return attrs

    def create(self, validated_data):
        """ Securely creates user with hashed password """
        validated_data.pop('password2')
        validated_data['email'] = validated_data['email'].lower().strip()  # ✅ Normalize email before saving
        return CustomUser.objects.create_user(**validated_data)


# ✅ Handles User Authentication
class LoginSerializer(serializers.Serializer):
    """ 
    - Validates credentials
    - Normalizes username input
    - Checks account status before login
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """ Authenticates user and checks account status """
        username = data["username"].strip().lower()
        password = data["password"]

        user = CustomUser.objects.filter(username__iexact=username).first()  # ✅ Case-insensitive lookup

        if not user or not authenticate(username=username, password=password):
            raise serializers.ValidationError("Invalid credentials")  # ✅ Prevents username/password enumeration

        if not user.is_active:
            raise serializers.ValidationError("Account is inactive. Please verify your email.")  # ✅ Helps inactive users

        return user


# ✅ Handles Password Reset Request via Email
class PasswordResetRequestSerializer(serializers.Serializer):
    """ 
    - Accepts user's email for password reset request 
    - Ensures email exists in the system 
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """ Validates whether email exists in the system """
        if not CustomUser.objects.filter(email__iexact=value.lower().strip()).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return value.lower().strip()


# ✅ Handles Password Reset Confirmation & Updates User's Password
class PasswordResetConfirmSerializer(serializers.Serializer):
    """ 
    - Accepts new password for resetting user credentials 
    - Enforces strong password requirements 
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]  # ✅ Uses Django's built-in validation
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """ Validates if passwords match """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        return attrs