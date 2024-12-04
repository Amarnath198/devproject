from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Department, Event, Enrollment, EventImage, EventType

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_type', 'start_date', 'end_date', 'organized_by', 'incharge', 'description', 'venue']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded-lg p-2'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded-lg p-2'}),
        }

class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ['image']
       

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = '__all__'

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['event']

class EnrollmentConfirmationForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['is_confirmed']
