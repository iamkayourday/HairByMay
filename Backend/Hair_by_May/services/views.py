from requests import Response
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.views import APIView
import stripe
from django.conf import settings
from django.http import response
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Service, Category, AppointmentOption, Booking, ContactSubmission
from .serializers import ServiceSerializer, CategorySerializer, AppointmentOptionSerializer, BookingSerializer, ContactSerializer
# from .permissions import IsAdminUser  # Import the custom permission
from rest_framework import serializers


stripe.api_key = settings.STRIPE_SECRET_KEY

# Service Views
class ServiceCreateView(CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 

class ServiceUpdateView(UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes =  [IsAuthenticated, IsAdminUser] 

class ServiceDeleteView(DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 

class ServiceListView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]  

class ServiceDetailView(RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]  

# Repeat for Category and AppointmentOption
class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  

class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 

class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  

class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  

class AppointmentOptionCreateView(CreateAPIView):
    queryset = AppointmentOption.objects.all()
    serializer_class = AppointmentOptionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  

class AppointmentOptionUpdateView(UpdateAPIView):
    queryset = AppointmentOption.objects.all()
    serializer_class = AppointmentOptionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 

class AppointmentOptionDeleteView(DestroyAPIView):
    queryset = AppointmentOption.objects.all()
    serializer_class = AppointmentOptionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  
class AppointmentOptionListView(ListAPIView):
    queryset = AppointmentOption.objects.all()
    serializer_class = AppointmentOptionSerializer
    permission_classes = [AllowAny]  

class AppointmentOptionDetailView(RetrieveAPIView):
    queryset = AppointmentOption.objects.all()
    serializer_class = AppointmentOptionSerializer
    permission_classes = [AllowAny]  



# Booking Views
from rest_framework.exceptions import ValidationError
from datetime import datetime

class BookingCreateView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        preferred_date = serializer.validated_data['preferred_date']
        preferred_time = serializer.validated_data['preferred_time']
        now = datetime.now()

        # Convert preferred_date and preferred_time into a full datetime object
        selected_datetime = datetime.combine(preferred_date, preferred_time)

        # Prevent booking for past dates and times
        if selected_datetime < now:
            raise ValidationError("You cannot book a past date or time. Please select a future slot.")

        # Prevent duplicate bookings for the same date/time
        if Booking.objects.filter(preferred_date=preferred_date, preferred_time=preferred_time).exists():
            raise ValidationError("This date and time are already booked. Please select another.")

        # Assign user or keep it as guest booking
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)

class BookingUpdateView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()  # Admins can update any booking
        return Booking.objects.filter(user=self.request.user)  # Users update only their own bookings
    def perform_update(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save(user=None)


class BookingCancelView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.instance.status = "canceled"
        serializer.save()
 
 
class BookingListView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]   

class BookingDetailView(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]   

# class BookingUserListView(ListAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated]  

#     def get_queryset(self):
#         user = self.request.user
#         return Booking.objects.filter(user=user)  
    

class BookingUserListView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)  # Restrict to logged-in user's bookings


class BookingPaymentView(APIView):
    permission_classes = [AllowAny]  # Only logged-in users can pay

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            
            # Create Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Booking for {booking.service.title}',
                        },
                        'unit_amount': int(booking.total_cost * 100),  # Convert to cents
                    },
                    'quantity': 1,
                }],
                metadata={'booking_id': str(booking.id)},
                mode='payment',
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=settings.STRIPE_CANCEL_URL,
            )
            
            return Response({'url': session.url})
        
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=404)

class ContactCreateView(CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSerializer
    permission_classes = []  # Allow public submissions

    def perform_create(self, serializer):
        try:
            submission = serializer.save()
            
            # Email to ADMIN
            admin_subject = f"📬 New Contact Submission: {submission.name}"
            admin_message = f"""
            Name: {submission.name}
            Email: {submission.email}
            Phone: {submission.phone or 'Not provided'}
            
            Message:
            {submission.message}
            """
            
            # Email to USER
            user_subject = "Thank you for contacting HairByMay!"
            user_message = f"""
            Hi {submission.name},
            
            We've received your message and will respond within 24-48 hours.
            
            Your Query:
            "{submission.message[:100]}{'...' if len(submission.message) > 100 else ''}"
            
            Best regards,
            The HairByMay Team
            """

            # Send both emails (wrapped in try-except for individual failures)
            try:
                send_mail(
                    subject=admin_subject,
                    message=admin_message.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
            except Exception as admin_error:
                print(f"Failed to send admin email: {admin_error}")

            try:
                send_mail(
                    subject=user_subject,
                    message=user_message.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[submission.email],
                    fail_silently=False,
                )
            except Exception as user_error:
                print(f"Failed to send user confirmation: {user_error}")

        except Exception as e:
            print(f"Contact submission failed: {e}")
            raise  # Re-raise to return 400 error to client

# List all contact submissions
class ContactListView(ListAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]  # Only admins can view all submissions