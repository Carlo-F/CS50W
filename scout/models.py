from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class EducationalGoal(models.Model):
    EDUCATIONAL_GOALS = [
        (
            "1. Impegno Civile",
            (
               ("1.1", "Impegno per la legalità e la difesa dei diritti"),
               ("1.2", "Partecipazione e cittadinanza attiva"),
               ("1.3", "Sensibilità, attenzione e rispetto verso l’ambiente"),
               ("1.4", "Adottare stili di vita sostenibili e solidali"),
               ("1.5", "Interpretare criticamente i messaggi sociali"),
               ("1.6", "Valorizzare e integrare le diversità"),
               ("1.7", "Impegno per la pace"),
            ),
        ),
        (
            "2. Corporietà",
            (
                ("2.1", "Consapevolezza e sviluppo di se', dei propri limiti e delle proprie potenzialita'"),
                ("2.2", "Adozione di stili di vita sani"),
                ("2.3", "Corporeità nelle relazioni"),
            ),
        ),
        (
            "3. Creatività",
            (
                ("3.1", "Originalità e Fantasia"),
                ("3.2", "Capacità progettuali"),
                ("3.3", "Capacità operative"),
                ("3.4", "Sostenibilità nella gestione delle risorse"),
            ),
        ),
        (
            "4. Carattere",
            (
                ("4.1", "Educazione all’impegno e alla responsabilità"),
                ("4.2", "Sviluppo del senso critico"),
                ("4.3", "Vivere i valori"),
                ("4.4", "Gestione delle emozioni"),
                ("4.5", "Saper comunicare"),
                ("4.6", "Sensibilità, attenzione e rispetto verso se stessi e verso gli altri"),
                ("4.7", "Saper collaborare"),
            ),
        ),
        (
            "5. Dimensione spirituale",
            (
                ("5.1", "Sviluppare una ricerca personale"),
                ("5.2", "Saper dare un senso alle proprie esperienze e ai propri vissuti"),
                ("5.3", "Coerenza nelle scelte"),
            ),
        ),
    ]

class Activity(models.Model):
    title = models.CharField(max_length=180)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="activities")
    AGE_RANGES = [
        ("lupetti", "Lupetti (8-11 years)"),
        ("esploratori", "Esploratori (12-15 years)"),
        ("rover", "Rover (16-19 years)"),
    ]
    LOCATIONS = [
        ("indoor", "indoor activity"),
        ("outdoor", "outdoor activity"),
        ("online", "online activity"),
        ("in-person", "in-person activity"),
    ]
    GAME_MODES = [
        ("team", "Team"),
        ("unit", "Unit"),
        ("single", "Single")
    ]
    age_range = models.CharField(max_length=80, choices=AGE_RANGES, default="lupetti")
    location = models.CharField(max_length=80, choices=LOCATIONS, default="outdoor")
    educational_goals = models.CharField(max_length=180, choices=EducationalGoal.EDUCATIONAL_GOALS)
    duration = models.IntegerField(help_text="Duration of the activity in minutes")
    required_materials = models.CharField(blank=True, max_length=180, default=None)
    method = models.TextField(default=None)
    game_mode = models.CharField(max_length=80, choices=GAME_MODES, default="team")
    is_suitable_for_disabled = models.BooleanField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    liked_activity = models.ForeignKey("Activity", on_delete=models.CASCADE, related_name="likers")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"'{self.user.username}' likes {self.liked_activity}"
