from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email,full_name=None,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError('User must have an email Address.')
        if not password:
            raise ValueError('User must have password')
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj
        
    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name = full_name,
            password=password,
            is_staff = True,
        )
        return user
        
    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff = True,
            is_admin = True,
        )
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    full_name = models.CharField(max_length=255,blank=True,null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_active(self):
        return self.active
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_staff(self):
        return self.staff