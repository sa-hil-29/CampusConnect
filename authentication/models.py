from django.contrib.auth.models import AbstractUser
from django.db import models
import bcrypt
from django.db.models.signals import pre_save
from django.dispatch import receiver


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("admin", "Placement Officer"),
        ("company", "Company"),
    ]

    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=128)  # bcrypt hash
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "role"]

    class Meta:
        db_table = "users"
        constraints = [
            models.CheckConstraint(
                check=models.Q(role__in=["student", "admin", "company"]),
                name="valid_user_role",
            )
        ]

    def set_password(self, raw_password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode(), salt).decode()

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())

    @property
    def is_placement_officer(self):
        return self.role == "admin"

    @property
    def is_company(self):
        return self.role == "company"

    def save(self, *args, **kwargs):
        if self.role == "admin":
            self.is_staff = self.is_superuser = True
        else:
            self.is_staff = self.is_superuser = False
        super().save(*args, **kwargs)


@receiver(pre_save, sender=User)
def auto_username(sender, instance, **kwargs):
    if not instance.username and instance.email:
        base = instance.email.split("@")[0]
        name = base
        i = 1
        while User.objects.filter(username=name).exclude(pk=instance.pk).exists():
            name = f"{base}{i}"
            i += 1
        instance.username = name
