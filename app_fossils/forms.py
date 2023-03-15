from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from captcha.fields import CaptchaField

from .models import DBSpecies, DBFossil, Profile, DBFossilGathering, DBEvent, FossilEvent

class FormSpecies(forms.ModelForm):
    captcha = CaptchaField()
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
            'fossil_gathered':forms.Select(attrs={'class':'form-control'}),
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

class FormEmail(forms.Form):
    email = forms.EmailField()
    email_note = forms.CharField(widget=forms.Textarea, required=False)
    include_price = forms.BooleanField(required=False)

##########################################################
##########    P R O F I L E    S E C T I O N    ##########
##########################################################

class FormAccount(UserChangeForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        exclude = ('password', 'password1', 'password2', 'password3')


class FormProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user', )
        widgets = {
            'user_avatar':forms.FileInput(attrs={'class':'form-control'}),
            'user_additional_email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'user_website':forms.URLInput(attrs={'class':'form-control', 'placeholder':'Website'})
        }


################################################################
##########    G A T H E R I N G S    S E C T I O N    ##########
################################################################

class FormGathering(forms.ModelForm):
    class Meta:
        model = DBFossilGathering
        fields = "__all__"
        exclude = ("gathering_owner", 'gathering_slug')
        widgets = {
            'gathering_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'required'}),
            'gathering_date':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'gathering_image':forms.FileInput(attrs={'class':'form-control'}),
            'gathering_description':forms.Textarea(attrs={'class':'form-control'}),
            'gathering_location':forms.TextInput(attrs={'class':'form-control'}),
            'gathering_location_geological_time':forms.TextInput(attrs={'class':'form-control'}),
            'gathering_duration': forms.TextInput(attrs={'class': 'form-control'}),
            'gathering_pdf': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(FormGathering, self).__init__(*args, **kwargs)

########################################################
##########    E V E N T S    S E C T I O N    ##########
########################################################

class FormEvent(forms.ModelForm):
    class Meta:
        model = DBEvent
        fields = ['event_name', 'event_date', 'event_notes']
        widgets = {
            'event_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'required'}),
            'event_date':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'event_notes': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(FormEvent, self).__init__(*args, **kwargs)


class FormFossilEvent(forms.ModelForm):
    class Meta:
        model = FossilEvent
        fields = ('fossil', 'fossil_lending_date', 'fossil_lending_date_returned', 'fossil_lending_notes')


        widgets = {
            'fossil': forms.Select(attrs={'class': 'form-control'}),
            'fossil_lending_date':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'fossil_lending_date_returned':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'fossil_lending_notes': forms.Textarea(attrs={'class': 'form-control'}),
        }

class FormFossilReturn(forms.ModelForm):
    class Meta:
        model = FossilEvent
        fields = ('fossil_lending_date_returned',)

        widgets = {
            'fossil_lending_date_returned':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }