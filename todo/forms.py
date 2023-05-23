from django import forms
from . models import PendingJob


class PendingJobForm(forms.ModelForm):
    class Meta:
        model = PendingJob
        fields = ('station', 'job_title', 'problem_reported',
                  'part_required', 'assigned_by', 'job_status')
        widgets = {
            'station': forms.TextInput(attrs={'placeholder': 'Enter station name'}),
            'job_title': forms.Select(),
            'problem_reported': forms.Textarea(attrs={'placeholder': 'Describe problem reported'}),
            'part_required': forms.Textarea(attrs={'placeholder': 'List all parts required'}),
            'assigned_by': forms.Select(),
            'job_status': forms.CheckboxInput()
        }

    def __init__(self, *args, **kwargs):
        super(PendingJobForm, self).__init__(*args, **kwargs)
        self.fields['station'].label = ''
        self.fields['job_title'].label = ''
        self.fields['problem_reported'].label = ''
        self.fields['part_required'].label = ''
        self.fields['assigned_by'].label = ''
        self.fields['job_status'].label = 'Completed'

        self.fields['station'].widget.attrs['class'] = 'form-control'
        self.fields['job_title'].widget.attrs['class'] = 'form-select'
        self.fields['problem_reported'].widget.attrs['class'] = 'form-control'
        self.fields['part_required'].widget.attrs['class'] = 'form-control'
        self.fields['assigned_by'].widget.attrs['class'] = 'form-select'
        self.fields['job_status'].widget.attrs['class'] = 'form-check-input'
