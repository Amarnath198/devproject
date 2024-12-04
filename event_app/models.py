import uuid
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EventType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_id = models.CharField(max_length=8, unique=True, editable=False, default='')
    name = models.CharField(max_length=200)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    organized_by = models.ForeignKey(Department, on_delete=models.CASCADE)
    incharge = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    venue = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.event_id:
            self.event_id = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/')

    def __str__(self):
        return f"Image for {self.event.name}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} enrolled in {self.event.name}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

