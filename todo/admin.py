from django.contrib import admin
from .models import PendingJob, DepartmentHead


@admin.register(PendingJob)
class AdminPendingJob(admin.ModelAdmin):
    list_display = ('station', 'job_title', 'problem_reported',
                    'part_required', 'assigned_time', 'assigned_by',)
    search_fields = ('station', 'job_title', 'problem_reported',
                     'part_required', 'assigned_time', 'assigned_by',)
    sortable_by = ('station', 'job_title', 'problem_reported',
                   'part_required', 'assigned_time', 'assigned_by',)


@admin.register(DepartmentHead)
class AdminDepartmentHead(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    sortable_by = ('name',)
