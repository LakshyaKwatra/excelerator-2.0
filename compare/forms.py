from django import forms
from . import views
from upload.models import Upload

DEFAULT_CHOICE = '-----'
FILTER_CHOICES = [('View All', 'View All'),
                  ('View Unique', 'View Unique'),
                  ('View Same', 'View Same')]

class ComparisonForm(forms.Form):
    file1sheet = forms.ChoiceField(choices=[])
    file1column = forms.ChoiceField(choices=[])
    file2sheet = forms.ChoiceField(choices=[])
    file2column = forms.ChoiceField(choices=[])
    pivot_column = forms.ChoiceField(choices=[])
    filters = forms.ChoiceField(choices=FILTER_CHOICES)

    def __init__(self, *args, **kwargs):
        super(ComparisonForm, self).__init__(*args, **kwargs)
        self.fields['file1sheet'] = forms.ChoiceField(choices=self.get_choices_dict()['file1sheet_choices'])
        self.fields['file1sheet'].label = "First File Sheet"

        self.fields['file1column'] = forms.ChoiceField(choices=self.get_choices_dict()['file1column_choices'])
        self.fields['file1column'].label = "First File Column"
        self.fields['file1column'].widget.attrs['required'] = 'required'

        self.fields['file2sheet'] = forms.ChoiceField(choices=self.get_choices_dict()['file2sheet_choices'])
        self.fields['file2sheet'].label = "Second File Sheet"
        self.fields['file2column'] = forms.ChoiceField(choices=self.get_choices_dict()['file2column_choices'])
        self.fields['file2column'].label = "Second File Column"
        self.fields['pivot_column'] = forms.ChoiceField(choices=self.get_choices_dict()['pivot_column_choices'])
        self.fields['pivot_column'].label = "Pivot Column"
        self.fields['filters'].label = "Apply Filter"

    def get_choices_dict(self):
        object_data = views.get_object_data(Upload.objects.last())
        file1sheets = object_data['file1sheets']
        file2sheets = object_data['file2sheets']
        file1dropdown = object_data['file1dropdown']
        file2dropdown = object_data['file2dropdown']
        file1dropdown_dict = object_data['file1dropdown_dict']
        file2dropdown_dict = object_data['file2dropdown_dict']
        file1_is_xl = object_data['file1_is_xl']
        file2_is_xl = object_data['file2_is_xl']
        FILE1SHEET_CHOICES = [("", DEFAULT_CHOICE)]
        FILE2SHEET_CHOICES = [("", DEFAULT_CHOICE)]
        FILE1COLUMN_CHOICES = [("", DEFAULT_CHOICE)]
        FILE2COLUMN_CHOICES = [("", DEFAULT_CHOICE)]
        PIVOT_COLUMN_CHOICES = [("", 'No Pivot Required')]
        if file1_is_xl:
            for sheet in file1sheets:
                FILE1SHEET_CHOICES.append((sheet, sheet))
                for column in file1dropdown_dict[sheet]:
                    FILE1COLUMN_CHOICES.append((column, column))
                    PIVOT_COLUMN_CHOICES.append(('File-1: '+column, 'File-1: '+column))
        else:
            for column in file1dropdown:
                FILE1COLUMN_CHOICES.append((column, column))
                PIVOT_COLUMN_CHOICES.append(('File-1: '+column, 'File-1: '+column))
        if file2_is_xl:
            for sheet in file2sheets:
                FILE2SHEET_CHOICES.append((sheet, sheet))
                for column in file2dropdown_dict[sheet]:
                    FILE2COLUMN_CHOICES.append((column, column))
                    PIVOT_COLUMN_CHOICES.append(('File-2: '+column, 'File-2: '+column))
        else:
            for column in file2dropdown:
                FILE2COLUMN_CHOICES.append((column, column))
                PIVOT_COLUMN_CHOICES.append(('File-2: '+column, 'File-2: '+column))
        context = {}
        context['file1sheet_choices'] = FILE1SHEET_CHOICES
        context['file2sheet_choices'] = FILE2SHEET_CHOICES
        context['file1column_choices'] = FILE1COLUMN_CHOICES
        context['file2column_choices'] = FILE2COLUMN_CHOICES
        context['pivot_column_choices'] = PIVOT_COLUMN_CHOICES
        return context