from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.urls import reverse
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


User = get_user_model()


# ✅ RegisterView: Handles user registration & sends email verification
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.is_active = True  # ✅ Immediately activate user
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)



# ✅ VerifyEmailView: Handles email verification
class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        """
        - Decodes verification token
        - Activates user account if valid
        - Prevents re-verifying already verified accounts
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid token"}, status=400)

        if user.is_active:  # ✅ Prevent unnecessary verifications
            return Response({"message": "Email already verified"}, status=200)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully"}, status=200)

        return Response({"error": "Invalid or expired token"}, status=400)



# ✅ LoginView: Handles user authentication & prevents unverified users from logging in
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data  # Authenticated user
        
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_superuser': user.is_superuser  # ✅ Send role info
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)




# ✅ LogoutView: Logs out user by blacklisting their refresh token
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        - Blacklists the refresh token
        - Ensures user session is properly terminated
        """
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken(refresh_token)
            refresh.blacklist()

            return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({'error': 'Token blacklisting failed'}, status=status.HTTP_400_BAD_REQUEST)



# ✅ ProfileView: Allows authenticated users to retrieve & update their own profile
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        - Returns the user object making the request
        - Allows users to update their own profile
        """
        return self.request.user


# ✅ RefreshTokenView: Handles refreshing JWT access token
class RefreshTokenView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        - Accepts refresh token
        - Generates new access token if refresh token is valid
        """
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            return Response({'access': new_access_token}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)



# ✅ PasswordResetRequestView: Handles user password reset requests via email
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        - Generates password reset token
        - Sends reset link to user via email
        """
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:3000/reset-password/{uid}/{token}"

            send_mail(
                "Password Reset Request",
                f"Click the link below to reset your password:\n{reset_link}",
                "your-email@gmail.com",
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "Password reset link sent successfully."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)



# ✅ PasswordResetConfirmView: Handles password reset confirmation and updates user's password
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        """
        - Validates reset token
        - Updates user's password upon confirmation
        """
        new_password = request.data.get("password")
        if not new_password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid token or user not found"}, status=status.HTTP_400_BAD_REQUEST)