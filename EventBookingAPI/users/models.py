from django.db import models
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES=(
        ("user","User"),
        ("organizer","Organizer")
    )

    email=models.EmailField(unique=True)
    role=models.CharField(max_length=20,default="user",choices=ROLE_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS=['username']
    USERNAME_FIELD='email'

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    phone=PhoneNumberField(blank=True,unique=True,region="IN")
    date_of_birth=models.DateField(blank=True,null=True)
    address=models.CharField(max_length=255,blank=True)
    city=models.CharField(max_length=50,blank=True)
    country=models.CharField(max_length=50,blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
