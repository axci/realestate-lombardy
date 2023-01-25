from django import forms
from scraper.models import Apartment


class ApartmentForm(forms.Form):

    PROVINCE_CHOICES = (
        ('', '---'),
        (1, 'Bergamo'),
        (2, 'Brescia'),
        (3, 'Como'),
        (4, 'Cremona'),
        (5, 'Lecco'),
        (6, 'Lodi'),
        (7, 'Mantova'),
        (8, 'Milano'),
        (9, 'Monza e Brianza'),
        (10, 'Pavia'),
        (11, 'Sondrio'),
        (12, 'Varese'),
    )

    CONDITION_CHOICES = (
        ('', '---'),
        ('Ottimo / Ristrutturato', 'Ottimo / Ristrutturato'),
        ('Buono / Abitabile', 'Buono / Abitabile'),
        ('Nuovo / In costruzione', 'Nuovo / In costruzione'),
        ('Da ristrutturare', 'Da ristrutturare'),
    )

    TYPOLOGY_CHOICES = (
        ('', '---'),
        ('Appartamento', 'Appartamento'),
        ('Attico - Mansarda', 'Attico - Mansarda'),
        ('Casa indipendente', 'Casa indipendente'),
        ('Loft', 'Loft'),
        ('Rustico - Casale', 'Rustico - Casale'),
        ('Villa', 'Villa'),
        ('Villetta a schiera', 'Villetta a schiera',)
    )

    price_from = forms.IntegerField(required=False)
    price_to = forms.IntegerField(required=False)
    area_from = forms.IntegerField(required=False)
    area_to = forms.IntegerField(required=False)
    
    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    province = forms.ChoiceField(choices=PROVINCE_CHOICES, required=False)
    typology = forms.ChoiceField(choices=TYPOLOGY_CHOICES, required=False)