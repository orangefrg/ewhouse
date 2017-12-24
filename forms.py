from django import forms
from .models import Component, Location

class OperationForm(forms.Form):
    to_location = forms.ModelChoiceField(label="Перенести в",
                                        help_text="Выберите расположение, куда нужно перенести компоненты. "\
                                        "Поиск не будет выполняться в этом расположении", queryset=Location.objects.all(),
                                        required=False)
    component = forms.ModelChoiceField(label="Компонент", queryset=Component.objects.all(), empty_label=None)
    count = forms.IntegerField(label="Количество", min_value=1)

class ManualOperationForm(forms.Form):
    component = forms.ModelChoiceField(label="Компонент", queryset=Component.objects.all(), empty_label=None)
    location_count = forms.IntegerField(widget=forms.HiddenInput(), label="Расположения")

    def __init__(self, *args, **kwargs):
        location_count = 1
        if len(args) > 0 and args[0]["location_count"] is not None and int(args[0]["location_count"]) > 1:
            location_count = args[0]["location_count"]
        print(args)
        print(kwargs)
        super(ManualOperationForm, self).__init__(*args, **kwargs)
        self.fields['location_count'].initial = location_count
        print(self.fields)

        for i in range(int(location_count)):
            self.fields['location_{}'.format(i)] = forms.ModelChoiceField(
                label="Расположение {}".format(i+1),
                help_text="Расположение, где нужно найти компоненты",
                queryset=Location.objects.all())
            self.fields['count_{}'.format(i)] = forms.IntegerField(label="Количество", min_value=0)

    def get_location_tuples(self):
        cdata = self.cleaned_data
        out_data_dict = {}
        for i in range(int(cdata["location_count"])):
            cnt = cdata["count_{}".format(i)]
            loc = cdata["location_{}".format(i)]
            if loc is not None and cnt > 0:
                if loc in out_data_dict:
                    out_data_dict[loc] += cnt
                else:
                    out_data_dict[loc] = cnt
        return out_data_dict.items()

