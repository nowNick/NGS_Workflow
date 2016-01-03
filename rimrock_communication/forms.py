from django import forms

from .models import Job, UserProxy


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('job_name', 'sequence_read_url', 'output_file_path', 'workspace_directory')

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['output_file_path'].required = False
        self.fields['workspace_directory'].required = False


class UserProxyForm(forms.ModelForm):
    class Meta:
        model = UserProxy
        fields = ('proxy',)
