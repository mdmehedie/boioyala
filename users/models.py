from django.db import models 
from .managers import UserManager
from django.contrib.auth.models import (
    AbstractBaseUser
)
from django.utils.html import format_html
from django.core.exceptions import ValidationError
 
class Institute(models.Model):
    name=models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.name     



class Interest(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name 
 

class User(AbstractBaseUser):
    email = models.EmailField(unique=True) 
    full_name=models.CharField(max_length=255) 
    avatar=models.ImageField(upload_to="media/profile",default="media/default/profile_avatar.png")
    phone=models.CharField(max_length=255,blank=True,null=True)
    phone_verified_at=models.DateTimeField(auto_now=True)
    address=models.CharField(max_length=1000)
    city=models.CharField(max_length=255)
    upazila=models.CharField(max_length=255) 
    district=models.CharField(max_length=255)
    institute=models.ForeignKey(Institute,on_delete=models.DO_NOTHING,blank=True,null=True)
    interest=models.ForeignKey(Interest,on_delete=models.DO_NOTHING,blank=True,null=True)
    occupation=models.CharField(max_length=255,blank=True,null=True)
    gender=models.CharField(max_length=255,choices=(
        ("Male","Male"),
        ("Female","Female"),
        ("Others","Others"),
    ),blank=True,null=True)
    total_donation=models.PositiveBigIntegerField(default=0)
    description=models.TextField(default="bio...")

    account_type =models.CharField(max_length=1,choices=(
        ("1","Administrator"),
        ("2","Donar"),
         )
         ,default="2")
    
    otp=models.PositiveBigIntegerField(blank=True,null=True)
    url=models.CharField(max_length=255,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)

    is_superuser=models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_disabled=models.BooleanField(default=False) 
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin 

    def avatar_circle(self):
        return format_html(f"<img src='{self.avatar.url}' style='width:25px;border-radius:50%'>")

    class Meta:
        db_table="users"

    def save(self,*args,**kwargs):
        if not self.url:
            self.url=str(self.email).split("@")[0]
        return super().save(*args,**kwargs) 
    
    
    
    





