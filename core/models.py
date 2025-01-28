from django.db import models

from accounts.models import User


class Defi(models.Model):
    CATEGORIE_CHOICES = [
        ('Debutant', 'Débutant'),
        ('Intermediaire', 'Intermédiaire'),
        ('Avance', 'Avancé'),
    ]

    titre = models.CharField(max_length=255)
    description = models.TextField()
    difficulte = models.CharField(max_length=50, choices=[('facile', 'Facile'), ('moyen', 'Moyen'), ('difficile', 'Difficile')])
    points = models.PositiveIntegerField()
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    flag = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
    
    def set_points(self):
        if self.categorie == 'Debutant':
            self.points = 200
        elif self.categorie == 'Intermediaire':
            self.points = 450
        elif self.categorie == 'Avance':
            self.points = 800
        self.save()

class Soumission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    defi = models.ForeignKey(Defi, on_delete=models.CASCADE)
    flag_soumis = models.CharField(max_length=255)
    date_soumission = models.DateTimeField(auto_now_add=True)
    est_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Soumission de {self.user.username} pour {self.defi.titre}"
    
    def verifier_flag(self):
        """Vérifie si le flag soumis est correct."""
        if self.flag_soumis == self.defi.flag:
            self.est_correct = True
            self.user.score.ajouter_points(self.defi.points)  # Ajout des points à l'utilisateur
            self.save()