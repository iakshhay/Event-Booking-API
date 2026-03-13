from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from users.models import User

# Create your models here.
class Event(models.Model):
    STATUS_CHOICES=(
        ("draft","Draft"),
        ("published","Published"),
        ("cancelled","Cancelled"),
        ("complete","Complete")
    )

    EVENT_TYPE_CHOICES=(
        ("music","Music"),
        ("comedy","Comedy"),
        ("talk","Talk"),
        ("spiritual","Spiritual")
    )

    LANGUAGE_CHOICES=(
        ("english","English"),
        ("hindi","Hindi"),
        ("marathi","Marathi"),
        ("tamil","Tamil"),
    )

    CITY_CHOICES=(
        ("pune","Pune"),
        ("delhi","Delhi"),
        ("mumbai","Mumbai"),
        ("chennai","Chennai"),
        ("kolkata","Kolkata")
    )

    organizer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='events')
    title=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255,unique=True)
    description=models.TextField()
    language=models.CharField(choices=LANGUAGE_CHOICES,max_length=50)
    event_type=models.CharField(choices=EVENT_TYPE_CHOICES,max_length=150)
    location=models.CharField(max_length=255)
    city=models.CharField(max_length=50,choices=CITY_CHOICES)
    max_capacity=models.PositiveIntegerField()
    available_seats=models.PositiveIntegerField()
    event_date_time=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.CharField(choices=STATUS_CHOICES,max_length=50,default="draft")

    def clean(self):
        if self.available_seats>self.max_capacity:
            raise ValidationError("Available seats cannot exceeds maximum capacity")
        if self.available_seats<=0:
            raise ValidationError("Available seats cannot be negative")

    def save(self,*args,**kwargs):
        if self._state.adding:
            self.available_seats=self.max_capacity
            
        if not self.slug:
            base_slug=slugify(self.title)
            slug=base_slug
            counter=1

            while Event.objects.filter(slug=slug).exists():
                slug =f"{base_slug}-{counter}"
                counter+=1

            self.slug=slug
        self.full_clean()
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title
    