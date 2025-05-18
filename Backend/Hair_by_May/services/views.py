from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Service, Category, AppointmentOption, Booking
from .serializers import ServiceSerializer, CategorySerializer, AppointmentOptionSerializer, BookingSerializer
from .permissions import IsAdminUser  # Import the custom permission
from rest_framework import serializers

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
    permission_classes = [IsAuthenticated, IsAdminUser]   

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
