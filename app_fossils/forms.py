from django import forms
from tinymce.widgets import TinyMCE

from .models import DBSpecies, DBFossil

class FormSpecies(forms.ModelForm):
    class Meta:
        model = DBSpecies
        fields = "__all__"
        exclude = ("species_owner", )
        widgets = {
            'species_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Species name (required)'}),
            'species_image':forms.FileInput(attrs={'class':'form-control'}),
            'species_description':forms.Textarea(attrs={'class':'form-control'}),
            'species_is_archived':forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super(FormSpecies, self).__init__(*args, **kwargs)

class FormFossil(forms.ModelForm):
    class Meta:
        model = DBFossil
        fields = "__all__"
        exclude = ("fossil_owner", "fossil_entry_created", "fossil_entry_updated", )
        widgets = {
            'fossil_species':forms.Select(attrs={'class':'form-control'}),
            'associated_fossils':forms.SelectMultiple(attrs={'class':'form-control'}),
            'fossil_status':forms.Select(attrs={'class':'form-control'}),
            'fossil_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'required'}),
            'fossil_description_short':forms.Textarea(attrs={'class':'form-control'}),
            'fossil_description_detailed':TinyMCE(),
            'fossil_is_favourite':forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fossil_age_in_years':forms.NumberInput(attrs={'class':'form-control'}),
            'fossil_value':forms.NumberInput(attrs={'class':'form-control'}),
            'fossil_condition':forms.Select(attrs={'class':'form-control'}),
            'fossil_date_acquired':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'fossil_size':forms.NumberInput(attrs={'class':'form-control'}),
            'fossil_weight':forms.NumberInput(attrs={'class':'form-control'}),
            'fossil_location':forms.TextInput(attrs={'class':'form-control'}),
            'fossil_location_latitude':forms.NumberInput(attrs={'class':'form-control'}),
            'fossil_location_longitude':forms.NumberInput(attrs={'class':'form-control'}),
            'fossil_image':forms.FileInput(attrs={'class':'form-control'}),
            'fossil_image_resized':forms.FileInput(attrs={'class':'form-control'}),
            'fossil_public_url':forms.URLInput(attrs={'class':'form-control'}),
            'fossil_collector_name':forms.TextInput(attrs={'class':'form-control'}),
            'fossil_collector_email':forms.EmailInput(attrs={'class':'form-control'}),
            'fossil_collector_phone':forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(FormFossil, self).__init__(*args, **kwargs)
        self.fields['fossil_species'].queryset = DBSpecies.objects.filter(species_owner=user, species_is_archived=False)
        self.fields['associated_fossils'].queryset = DBFossil.objects.filter(fossil_owner=user)
