from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from myapp.models import Offerta, Studente, Proposta, TIPOLOGIA_CHOICES


class AziendaForm(forms.Form):
    nome = forms.CharField(min_length=4, max_length=200)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    sede = forms.CharField(max_length=200)
    pIva = forms.CharField(max_length=30)
    email = forms.EmailField()


class DocenteForm(forms.Form):
    codice = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    nome = forms.CharField(max_length=200)
    cognome = forms.CharField(max_length=200)
    materia = forms.CharField(max_length=100)
    email = forms.EmailField()


class StudenteForm(forms.Form, forms.ModelForm):
    matricola = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    nome = forms.CharField(max_length=200)
    cognome = forms.CharField(max_length=200)
    email = forms.EmailField()
    anno_corso = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6), ])
    crediti = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(360), ])

    class Meta:
        model = Studente
        fields = ['corso']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class OffertaForm(forms.ModelForm):
    class Meta:
        model = Offerta
        fields = ['titolo', 'descrizione', 'docente', 'corso', 'durata']


class PropostaForm(forms.ModelForm):
    class Meta:
        model = Proposta
        fields = ['titolo', 'descrizione', 'corso', 'durata', 'tipologia']

    def clean(self):
        durata = self.cleaned_data.get('durata')
        tipologia = self.cleaned_data.get('tipologia')

        if tipologia == TIPOLOGIA_CHOICES[0][0]:
            if durata != 0:
                raise ValidationError("Avendo scelto tipologia tesi, la durata deve essere zero")
        elif tipologia == TIPOLOGIA_CHOICES[1][1]:
            if durata == 0:
                raise forms.ValidationError("Avendo scelto tipologia attività progettuale, la durata non può essere zero")
