import uuid

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils.timezone import now


class Covoitureur(models.Model):
    adresse = models.CharField(max_length=255, null=True)
    cni = models.CharField(max_length=13, null=True)
    permis = models.ImageField(upload_to='permis', null=True)
    telephone = models.CharField(max_length=13, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def is_verified(self):
        return self.permis is not None

    def __str__(self):
        return self.user.username + '-Covoitureur'


class Vehicule(models.Model):
    CHOIX_COULEURS = [
        ('BL', 'Bleu'),
        ('B', 'Blanc'),
        ('N', 'Noir'),
        ('O', 'Orange'),
        ('R', 'Rouge'),
        ('V', 'Vert'),
        ('Vl', 'Violet'),
        ('J', 'Jaune'),
        ('G', 'Grise'),
        ('Cf', 'Café')
    ]

    numero_matricule = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True)
    immatriculation = models.CharField(max_length=7)
    couleur = models.CharField(max_length=255, choices=CHOIX_COULEURS, null=True)
    model = models.CharField(max_length=13, null=True)
    marque = models.CharField(max_length=13, null=True)
    climatisation = models.BooleanField(null=True)
    cni = models.CharField(max_length=13, null=True)
    Assurance = models.ImageField(upload_to='permis', null=True)
    covoitureur = models.ForeignKey(Covoitureur, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=now())
    updated_at = models.DateTimeField(auto_now=now())

    def __str__(self):
        return str(self.marque) + ' ' + str(self.model) + ' ' + str(self.immatriculation) + ' ' + str(self.couleur)


class VoyageCv(models.Model):
    num_voyagecv = models.UUIDField(default=uuid.uuid4, editable=True)
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
    covoitureur = models.ForeignKey(Covoitureur, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=now())
    updated_at = models.DateTimeField(auto_now=now())

    def save(self, *args, **kwargs):
        self.place_dispo = self.place_dispo - 1
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.ville_depart + '-' + self.ville_arrivee + '_' + str(self.date) + '_' + str(self.heure_depart)


class Prepaiement(models.Model):
    num_voyagecv = models.UUIDField(default=uuid.uuid4, editable=True)
    montant = models.PositiveIntegerField(default=0)
    date = models.DateField()
    status = models.BooleanField(null=True)


class ReservationCv(models.Model):
    num = models.UUIDField(default=uuid.uuid4, editable=True)
    mbre_place = models.PositiveSmallIntegerField()
    voyage = models.ForeignKey(VoyageCv, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=now()).auto_now
    updated_at = models.DateTimeField(auto_now=now())

    def reserver(self, *args, **kwargs):
        self.voyage.place_dispo -= 1
        self.voyage.save(*args, **kwargs)

    def __str__(self):
        return self.num + '-' + self.voyage.__str__()
