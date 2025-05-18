from rest_framework import serializers
from .models import Service, Category, AppointmentOption, Booking

class AppointmentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentOption
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    appointment_options = AppointmentOptionSerializer(many=True)  # Nest appointment options
    
    class Meta:
        model = Service
        fields = ['id', 'title', 'price', 'duration', 'description', 'appointment_options']  # Keep only relevant fields

class CategorySerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)  # Nest services inside categories

    class Meta:
        model = Category
        fields = ['id', 'name', 'services']  # Ensure services appear inside categories


# class BookingSerializer(serializers.ModelSerializer):
#     service = ServiceSerializer()  # Embed service details in booking response

#     class Meta:
#         model = Booking
#         fields = '__all__'

#     def get_total_price(self, obj):
#         base_price = obj.service.price
#         extra_cost = sum(option.extra_cost for option in obj.selected_options.all())
#         return base_price + extra_cost
    

class BookingSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)  # Show full service details
    selected_options = AppointmentOptionSerializer(many=True, read_only=True)  # Show selected add-ons
    total_price = serializers.SerializerMethodField()  # Calculate total cost

    class Meta:
        model = Booking
        fields = [
            'id', 'service', 'selected_options', 'full_name', 'email', 'phone',
            'preferred_date', 'preferred_time', 'status', 'total_price'
        ]

    def get_total_price(self, obj):
        base_price = obj.service.price  # Base price from service
        extra_cost = sum(option.extra_cost for option in obj.selected_options.all())  # Fix reference
        return base_price + extra_cost  # Calculate total price correctly