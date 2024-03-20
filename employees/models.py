from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator
from utilities.password import get_password_help_text, get_password_pattern

class Department(models.Model):
    department_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.department_name}'


class EmployeePosition(models.Model):
    employee_position_title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.employee_position_title}'
    

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You have not provided an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, **extra_fields)
    

class Employee(AbstractBaseUser, PermissionsMixin):
    password_help_text = get_password_help_text()

    # Regex pattern for password validation
    password_validator = RegexValidator(
        regex=get_password_pattern(),
        message=password_help_text
    )

    email = models.EmailField(default='', unique=True, verbose_name='Email Address')
    first_name = models.CharField(max_length=255, default='', verbose_name='First Name')
    last_name = models.CharField(max_length=255, default='', verbose_name='Last Name')

    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
    employee_position = models.ForeignKey(EmployeePosition, on_delete=models.PROTECT, null=True, blank=True)

    contact_no = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True, blank=True, verbose_name='Is Active')
    is_superuser = models.BooleanField(default=False, blank=True, verbose_name='Is Superuser')
    is_staff = models.BooleanField(default=False, blank=True, verbose_name='Is Staff')

    date_joined = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Date Joined')
    last_login = models.DateTimeField(blank=True, null=True, editable=False, verbose_name='Last Login')

    password = models.CharField(
        validators=[password_validator], 
        max_length=128,
        help_text=password_help_text
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self) -> str:
        return f'ID: {self.pk} - {self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]
    
    def validate(self, exclude=None):
        # Call the parent validate method
        super().validate(exclude=exclude)

        # Validate the password field
        self.password_validator(self.password, self)


# class Employee(models.Model):
#     user = models.OneToOneField(User,
#                                 on_delete=models.PROTECT,
#                                 null=True,
#                                 blank=True,
#                                 unique=True,
#                                 help_text='Click user to edit username, password, first and last name, staff status')
#     department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
#     employee_position = models.ForeignKey(EmployeePosition, on_delete=models.PROTECT, null=True, blank=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     contact_no = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return f'ID: {self.pk} - {self.first_name} {self.last_name}'