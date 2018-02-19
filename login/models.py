from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

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

    # TODO: implement method
    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        :param perm: permission
        :param obj:
        """
        return True

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


class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, first_name, last_name, password=None):
        """
        Creates and saves a CustomUser with the given email, date of birth, password,
        first name and last name.
        :param email:
        :param date_of_birth:
        :param password:
        :param first_name:
        :param last_name:
        :return:
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the
        :param email:
        :param date_of_birth:
        :param password:
        :return:
        """