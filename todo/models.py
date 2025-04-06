from django.db import models
from datetime import timedelta
from django.utils import timezone  # Import timezone

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Timer-related fields
    timer_start = models.DateTimeField(null=True, blank=True)
    timer_end = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0)

    def start_timer(self):
        """Sets the start time of the timer"""
        if not self.timer_start:
            self.timer_start = timezone.now()  # Get current time
        self.save()

    def stop_timer(self):
        """Sets the end time of the timer"""
        if not self.timer_end:
            self.timer_end = timezone.now()  # Get current time
        self.save()

    def get_timer_duration(self):
        """Calculate the duration of the timer."""
        if self.timer_start and self.timer_end:
            return self.timer_end - self.timer_start
        elif self.timer_start:
            # Timer is still running
            return timezone.now() - self.timer_start
        return timedelta(0)

    def __str__(self):
        return self.title
