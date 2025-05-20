import datetime
from django import forms
from .models import Destination, Itinerary, Budget, PackingItem

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'country', 'description', 'best_time_to_visit']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['destination', 'title', 'date', 'activities']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'activities': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['destination'].queryset = Destination.objects.filter(user=user)

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['destination', 'total_budget', 'accommodation', 'transportation', 'food', 'activities', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['destination'].queryset = Destination.objects.filter(user=user)

class PackingItemForm(forms.ModelForm):
    class Meta:
        model = PackingItem
        fields = ['destination', 'name', 'category']
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['destination'].queryset = Destination.objects.filter(user=user)







class HotelSearchForm(forms.Form):
    country = forms.CharField(max_length=100, required=True, label="Enter Country")


