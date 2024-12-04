from django.contrib import admin
from .models import Event, Department, EventType, Enrollment, Notification


models = [Event, Department, EventType, Enrollment, Notification]
for model in models:
    admin.site.register(model)
