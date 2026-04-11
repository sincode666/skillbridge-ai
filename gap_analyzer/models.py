from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class CompanyDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, default="Not Found")
    role = models.CharField(max_length=200, default="Not Found")
    company_skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"


class SkillGap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    missing_skills = models.TextField()
    verdict = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.verdict}"