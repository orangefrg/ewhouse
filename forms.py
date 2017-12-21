from django import forms
from .models import Component, Location

class OperationForm(forms.Form):
    to_location = forms.ModelChoiceField(label="Перенести в",
                                        help_text="Выберите расположение, куда нужно перенести компоненты. "\
                                        "Поиск не будет выполняться в этом расположении", queryset=Location.objects.all(),
                                        required=False)
    component = forms.ModelChoiceField(label="Компонент", queryset=Component.objects.all(), empty_label=None)
    count = forms.IntegerField(label="Количество", min_value=1)
