from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Contact, SpamReport

User = get_user_model()

# Serializing the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'phone_number', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False, 'allow_blank': True},
        }
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError({"error" :"This email is already in use."})
        return value

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValidationError({"error" :"Phone number must be exactly 10 digits."})
        if User.objects.filter(phone_number=value).exists():
            raise ValidationError({"error" :"This phone number is already in use."})
        return value
    
    def validate_username(self, value):
        if not value.strip():
            raise ValidationError({"error": "Username cannot be empty."})
        if len(value) < 3:
            raise ValidationError({"error": "Username must be at least 3 characters long."})
        if User.objects.filter(username=value).exists():
            raise ValidationError({"error": "This username is already in use."})
        return value
    
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError({"error": "Name cannot be empty."})
        if len(value) < 3:
            raise ValidationError({"error": "Name must be at least 3 characters long."})
        return value

    def create(self, validated_data):
        # Extract the required fields
        username = validated_data.get('username')
        password = validated_data.get('password')
        name = validated_data.get('name')
        phone_number = validated_data.get('phone_number')
        email = validated_data.get('email', None)  # Default to None if not provided

        # Create the user with the extracted fields
        user = User(
            username=username,
            name=name,
            phone_number=phone_number,
            email=email
        )
        user.set_password(password)
        user.save()
        return user

# Serializing the Contact model
class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nesting UserSerializer
    class Meta:
        model = Contact
        fields = ['id', 'user', 'name', 'phone_number']
        extra_kwargs = {'user': {'read_only': True}}

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValidationError({"error" :"Phone number must be exactly 10 digits."})
        if Contact.objects.filter(phone_number=value).exists():
            raise ValidationError({"error" :"This phone number is already in use."})
        return value
    
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError({"error" : "Name cannot be empty."})
        if len(value) < 3:
            raise ValidationError({"error" :"Name must be at least 3 characters long."})
        # if Contact.objects.filter(name=value).exists():
        #     raise ValidationError({"error" :"This name is already in use."})
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    
# Serializing the SpamReport model   
class SpamReportSerializer(serializers.ModelSerializer):
    reported_by = UserSerializer(read_only=True)  # Nesting UserSerializer

    class Meta:
        model = SpamReport
        fields = ['id', 'phone_number', 'reported_by', 'created_at']
        extra_kwargs = {'reported_by': {'read_only': True}}
        
    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValidationError({"error" :"Phone number must be exactly 10 digits."})
        return value    

    def create(self, validated_data):
        user = self.context['request'].user
        phone_number = validated_data['phone_number']

        # Check if the user has already reported this phone number
        if SpamReport.objects.filter(reported_by=user, phone_number=phone_number).exists():
            raise ValidationError({"error": "You have already reported this phone number."})

        # Check if the user is reporting their own phone number
        if user.phone_number == phone_number:
            raise ValidationError({"error": "You cannot report your own phone number."})


        validated_data['reported_by'] = user
        return super().create(validated_data)
    
    # def delete(self, report_id):
    #     user = self.context['request'].user
    #     print(report_id)
    #     print(user)
    #     try:
    #         spam_report = SpamReport.objects.get(pk=report_id, reported_by=user)
    #     except SpamReport.DoesNotExist:
    #         raise ValidationError({"error": "Report not found."})

    #     spam_report.delete()
    #     return {
    #         "message": "Successfully deleted report.",
    #         "report": SpamReportSerializer(spam_report).data
    #     }