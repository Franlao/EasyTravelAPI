import uuid

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils.timezone import now


class Compagnie(models.Model):
    adresse = models.CharField(max_length=255, null=True)
    nom_compagnie = models.CharField(max_length=13, null=True)
    cart_emtreprise = models.ImageField(upload_to='permis', null=True)
    telephone = models.CharField(max_length=13, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def is_verified(self):
        return self.cart_emtreprise is not None


class Voyage(models.Model):
    num_voyage = models.UUIDField(default=uuid.uuid4, editable=True)
    date = models.DateField()  # default=now().strftime("%Y-%m-%d")
    heure_depart = models.TimeField(null=True)
    lieu_depart = models.CharField(max_length=255)
    lieu_arrive = models.CharField(max_length=255)
    ville_depart = models.CharField(max_length=255)
    ville_arrivee = models.CharField(max_length=255)
    prix = models.PositiveIntegerField(default=0)
    place_dispo = models.PositiveSmallIntegerField(default=0)
    climatisation = models.BooleanField(null=True)
    wifi = models.BooleanField(null=True)
    repas = models.BooleanField(null=True)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=now())
    updated_at = models.DateTimeField(auto_now=now())

    def save(self, *args, **kwargs):
        self.place_dispo = self.place_dispo - 1
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.ville_depart + '-' + self.ville_arrivee + '_' + str(self.date) + '_' + str(self.heure_depart)


class Reservation(models.Model):
    num = models.UUIDField(default=uuid.uuid4, editable=True)
    mbre_place = models.PositiveSmallIntegerField()
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=now()).auto_now
    updated_at = models.DateTimeField(auto_now=now())

    def reserver(self, *args, **kwargs):
        self.voyage.place_dispo -= 1
        self.voyage.save(*args, **kwargs)

    @property
    def __str__(self):
        return self.num + '-' + str(self.voyage.__str__())
