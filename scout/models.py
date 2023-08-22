from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class EducationalGoal(models.Model):
    # todo: finish list
    EDUCATIONAL_GOALS = [
        (
            "1. Impegno Civile",
            (
               ("1.1", "Impegno per la legalita' e la difesa dei diritti"),
               ("1.2", "Partecipazione e cittadinanza attiva") 
            ),
        ),
        (
            "2. Corporieta'",
            (
                ("2.1", "Consapevolezza e sviluppo di se', dei propri limiti e delle proprie potenzialita'"),
                ("2.2", "Adozione di stili di vita sani")
            ),
        ),
    ]

class Activity(models.Model):
    title = models.CharField(max_length=180)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="activities")
    AGE_RANGES = [
        ("L", "Lupetti"),
        ("E", "Esploratori"),
        ("R", "Rover"),
    ]
    LOCATIONS = [
        ("ID", "indoor activity"),
        ("OD", "outdoor activity"),
        ("OL", "online activity"),
        ("IP", "in-person activity"),
    ]
    GAME_MODES = [
        ("T", "TEAM"),
        ("U", "UNIT"),
        ("S", "SINGLE")
    ]
    age_range = models.CharField(max_length=1, choices=AGE_RANGES, default="L")
    location = models.CharField(max_length=2, choices=LOCATIONS, default="OD")
    educational_goals = models.CharField(max_length=180, choices=EducationalGoal.EDUCATIONAL_GOALS)
    duration = models.IntegerField(help_text="Duration of the activity in minutes")
    required_materials = models.CharField(blank=False, max_length=180, default=None)
    method = models.TextField(default=None)
    game_mode = models.CharField(max_length=1, choices=GAME_MODES, default="T")
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
