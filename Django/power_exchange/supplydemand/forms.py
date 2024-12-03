from django import forms
from .models import FiveMSupplyDemand

class FiveMSupplyDemandForm(forms.ModelForm):
    class Meta:
        model = FiveMSupplyDemand
        fields = [ 'suppAbility', 'currPwrTot']

