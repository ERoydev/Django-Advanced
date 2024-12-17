from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model, models as auth_models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.hashers import make_password

# Just a proxy implementation demo
# class AccountsUserProxy(UserModel):
#     # age = models.IntegerField() # will not work
#     '''
#         Here i can just add methods or ordering to my UserModel
#     '''
#     class Meta:
#         proxy = True
#         ordering = ['username']
#

'''
1. Use the default user as-is
2. Extend the default user and add more stuff (Extend the 'AbstractUser' class)
3. Rewrite the whole user (Extend the 'AbstractBaseUser' class)
'''

# UserModel = get_user_model()


'''
1. Extend the build-in User model through 'AbstractUser':
    - Add 'age' field
    - Add 'gender' field
    - ...
Pros:
    - Simpler
    - No need to rewrite Django auth system
    - (Simple i will just introduce new User)

'''
# class AccountsUser(auth_models.AbstractUser):
#     age = models.PositiveIntegerField(
#         null=True,
#         blank=True
#     )


'''
# Better variation when i start project is this !
2. Extend the User model through a One-To-One relationship with a 'Profile' model:
    - Add 'age' field
    - Add 'gender' field
    - ...

2.1. Use the build-in user model for auth
'''
# The idea is to have model that store personal information
# and the User model will store only authentication credentials

# UserModel = get_user_model()
# class Profile(models.Model):
#     age = models.PositiveIntegerField(
#         blank=False,
#         null=False
#     )
#
#     # and i connect this personal info to it's User owner
#     user = models.OneToOneField(
#         UserModel,
#         on_delete=models.DO_NOTHING,
#         primary_key=True,
#     )
#     # profile_obj.pk == profile_obj.user_id

'''
2.2. Create our own user model

Pros:
    - Easier migration to other auth model in the future (!IMPORTANT and is a BIG PLUS ++)
'''
# UserModel = get_user_model()

# I create my Manager that inherit BaseUserManager and i just copy paste its functionality with little changes
class AccountUserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

# I should inherit permissions too to get all the permission methods
class AccountUser(auth_models.AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
     unique=True,
     error_messages={
         "unique": _("A user with that email already exists"),
     }
    )

    # This is the other (username) part of the **credentials**
    # Trqbva da go sloja to sochi kum emaila
    USERNAME_FIELD = "email"
    objects = AccountUserManager()

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)


class Profile(models.Model):
    age = models.PositiveIntegerField(
        blank=False,
        null=False
    )

    # and i connect this personal info to it's User owner
    user = models.OneToOneField(
        AccountUser,
        on_delete=models.DO_NOTHING,
        primary_key=True,
    )
    # profile_obj.pk == profile_obj.user_id
