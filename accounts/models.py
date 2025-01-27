from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Score(models.Model):
    RANK_CHOICES = [
        ('S', 'S'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    rank = models.CharField(max_length=1, choices=RANK_CHOICES, default='C')
    classement = models.IntegerField(default=0)

    def __str__(self):
        return f"Score de {self.user.username}: {self.points} points, Rang: {self.rank}"
    
    def ajouter_points(self, points):
        """Ajoute des points à l'utilisateur et met à jour son rang."""
        self.points += points
        self.save()
        self.update_rank()

    def update_rank(self):
        """Mise à jour automatique du rang et du classement"""
        # Mettre à jour le rang en fonction des points
        if self.points >= 8000:
            self.rank = 'A'
        elif self.points >= 4000:
            self.rank = 'B'
        else:
            self.rank = 'C'
        
        # Réajuster le classement global
        top_users = Score.objects.order_by('-points')[:5]
        for i, top_user in enumerate(top_users):
            top_user.rank = 'S'
            top_user.save()
        
        self.save()
