from django.contrib.auth.models import AbstractUser
from django.db import models
import bcrypt


class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("admin", "Admin"),
        ("company", "Company"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    email = models.EmailField(unique=True)

    def set_password(self, raw_password):
        super().set_password(
            raw_password
        )  # Uses Django's hasher (PBKDF2); for bcrypt, override if needed
        # Optional: Use bcrypt explicitly
        hashed = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt(12))
        self.password = hashed.decode("utf-8")

    def check_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode("utf-8"), self.password.encode("utf-8")
        )
