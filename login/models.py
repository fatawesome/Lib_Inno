from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.urls import reverse
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, address, password=None):
        """
        Creates and saves a CustomUser with the given email, password,
        first name and last name.
        :param email:
        :param password:
        :param first_name:
        :param last_name:
        :param phone_number
        :param address
        :return:
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, address, password):
        """
        Creates and saves a superuser with the
        :param address:
        :param phone_number:
        :param last_name:
        :param first_name:
        :param email:
        :param password:
        :return:
        """
        if len(CustomUser.objects.filter(is_admin=True)) + 1 > 1:
            raise ValidationError("Can only create 1 instance of Admin")

        user = self.create_user(email,
                                first_name=first_name,
                                last_name=last_name,
                                phone_number=phone_number,
                                address=address,
                                password=password,
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(max_length=500)
    subtype = models.CharField(max_length=20, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'address']

    objects = CustomUserManager()

    creator_email = models.CharField(max_length=50, null=True, blank=True, default="")

    def delete_user(self): # TODO Move it to user manager
        """
        Delete current user
        """
        self.delete()

    def get_absolute_url(self):
        """
        :return: the url to access a particular Document instance.
        """
        return reverse('customuser_detail', args=[str(self.id)])

    def get_full_name(self):
        """
        The user is identified by their email address
        :return: user email address
        """
        return self.email

    def get_short_name(self):
        """
        The user is identified by their email address
        :return: user email address
        """
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        :param perm: permission
        :param obj:
        """
        if self.is_admin or perm in self.get_all_permissions():
            return True
        return False

    # TODO: implement method
    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app 'app_label'?
        :param app_label: application
        """
        return True

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        """
        return self.is_admin



