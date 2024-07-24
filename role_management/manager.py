from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from role_management.models import Role

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, name, password=None, role=None, phone_number=None, **extra_fields):
        """
        Create and save a user with the given email, name, and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            name=name,
            role=role,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, role=None, **extra_fields):
        """
        Create and save a SuperUser with the given email, name, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        if role is None:
            role = Role.objects.get_or_create(name='superadmin')[0]

        return self.create_user(email, name, password, role, **extra_fields)
