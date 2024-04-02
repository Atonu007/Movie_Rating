from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    #Creates and saves a User with the given name,phone,password,email.
    def create_user(self, email, name, phone, password=None):
        
        if not email:
            raise ValueError('User must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),  # Normalize the email address to lowercase
            name=name,
            phone=phone,
        )

        # Set the password and save the user
        user.set_password(password)
        user.save(using=self._db)
        return user
   
    # Creates and saves a superuser with the given email, name and password.
    def create_superuser(self, email, name, phone, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone,
        )
        
        # Set the user as admin and save
        user.is_admin = True
        user.save(using=self._db)
        return user
    

# Custom User Model
class UserModel(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(unique=True,max_length=200)
    phone = models.CharField(unique=True,max_length=15)  
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()  # Use UserManager for managing users

    USERNAME_FIELD = 'email'  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = ['name', 'phone']  # Fields required when creating a user

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
