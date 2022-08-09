from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Types(models.TextChoices):
        PASSAGER = "PASSAGER", "Passager"
        COMPAGNIE = "COMPAGNIE", "Compagnie"
        COVOITUREUR = "COVOITUREUR", "Covoitureur"

    base_type = Types.PASSAGER

    # What type of user are we?
    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    # First Name and Last Name Do Not Cover Name Patterns
    # Around the Globe.
    solde = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.base_type
        return super().save(*args, **kwargs)


class PassagerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.PASSAGER)


class CompagnieManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COMPAGNIE)


class CovoitureurManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COVOITUREUR)


class SpyMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gadgets = models.TextField()


class Passager(User):
    base_type = User.Types.SPY
    objects = PassagerManager()

    class Meta:
        proxy = True

    def whisper(self):
        return "whisper"


class DriverMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    year = models.IntegerField()


class Compagnie(User):
    base_type = User.Types.DRIVER
    objects = CompagnieManager()

    @property
    def more(self):
        return self.drivermore

    class Meta:
        proxy = True

    def accelerate(self):
        return "Go faster"
