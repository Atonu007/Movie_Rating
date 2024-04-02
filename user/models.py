from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    #Creates and saves a User with the given name,phone,password,email.
    def create_user(self, email, name, phone, password=None):
        
        if not email:
            raise ValueError('User must have an email address')
        
        user = self.model(
            email=self.normalize_email(email), 
            name=name,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, phone, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone,
        )
       
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

    objects = UserManager()  

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['name', 'phone']  

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

class Movie(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True, related_name='movies')
    name = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()

    
    ratings = models.ManyToManyField('Rating', related_name='movies', blank=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='ratings_given')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} rated {self.movie.name} - {self.rating}"