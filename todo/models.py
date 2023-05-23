from django.db import models
from django.utils import timezone


class DepartmentHead(models.Model):
    title = [
        ('mr', 'MR'),
        ('mad', 'MADAM'),
        ('dir', 'DIRECTOR'),
        ('MD', 'MANAGER'),
    ]
    role = models.CharField(max_length=50, null=True,
                            blank=True, choices=title)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class PendingJob(models.Model):
    title_of_job = [
        ('FD', 'FUEL DISPENSER'),
        ('ELEC', 'ELECTRICALS'),
        ('TANK', 'TANK FARM'),
        ('GEN', 'GENERATOR'),
        ('LIGHTING', 'ELLUMINATION'),
        ('TOTTEM', 'FLAGPOLE'),
    ]
    station = models.CharField(max_length=50)
    job_title = models.CharField(
        max_length=50, choices=title_of_job, default='Fuel Dispenser')
    problem_reported = models.CharField(max_length=1080, null=True, blank=True)
    part_required = models.CharField(max_length=500, null=True, blank=True)
    assigned_time = models.DateTimeField(auto_now_add=timezone.now)
    assigned_by = models.ForeignKey(
        DepartmentHead, on_delete=models.CASCADE, default='Name')
    job_status = models.BooleanField(default=False)

    def __str__(self):
        return self.station
