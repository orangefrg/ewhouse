from django import forms
from .models import *
from .workers import get_availability_full

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


class MultipleOpsForm(forms.Form):
    target_location = forms.ModelChoiceField(label="Куда", queryset=Location.objects.all(), required=False, empty_label="Внешнее расположение")
    element_count = forms.IntegerField(widget=forms.HiddenInput(), label="Расположения")

    operation_type = forms.ChoiceField(label="Тип операции", choices = TRANSACTION_TYPES)

    def __init__(self, *args, **kwargs):
        element_count = 1
        if len(args) > 0 and args[0]["element_count"] is not None and int(args[0]["element_count"]) > 1:
            element_count = args[0]["element_count"]
        super(MultipleOpsForm, self).__init__(*args, **kwargs)
        self.fields['element_count'].initial = element_count

        for i in range(int(element_count)):
            self.fields['component_{}'.format(i)] = forms.ModelChoiceField(
                label="Компонент {}".format(i+1),
                help_text="Компонент, который требуется перенести",
                queryset=Component.objects.all())
            self.fields['location_{}'.format(i)] = forms.ModelChoiceField(
                label="Расположение {}".format(i+1),
                help_text="Расположение, где нужно найти компоненты",
                queryset=Location.objects.all())
            self.fields['count_{}'.format(i)] = forms.IntegerField(label="Количество", min_value=0)

    def get_ops_tuples_mult_in_one(self):
        cdata = self.cleaned_data
        out_data_dict = {}
        for i in range(int(cdata["element_count"])):
            loc = cdata["location_{}".format(i)]
            cnt = cdata["count_{}".format(i)]
            comp = cdata["component_{}".format(i)]
            if loc is not None and comp is not None and cnt > 0:
                if loc in out_data_dict:
                    if comp in out_data_dict[loc]:
                        out_data_dict[loc][comp] += cnt
                    else:
                        out_data_dict[loc][comp] = cnt
                else:
                    out_data_dict[loc] = {}
                    out_data_dict[loc][comp] = cnt
        return out_data_dict


    def get_availability(self):
        cdata = self.cleaned_data
        out = {}
        out["success"] = []
        out["failure"] = []
        t_loc = cdata["target_location"] 
        if cdata["operation_type"] in ["BUY", "GET", "MAKE"]:
            all_dict = self.get_ops_tuples_mult_in_one()
            comp_dict = {}
            for loc, comp_d in all_dict.items():
                for comp, cnt in comp_d.items():
                    if comp in comp_dict:
                        comp_dict[comp]["count"] += cnt
                    else:
                        comp_dict[comp] = {}
                        comp_dict[comp]["count"] = cnt
            for comp, comp_d in comp_dict.items():
                av = get_availability_full(comp, comp_d["count"], t_loc)
                comp_dict[comp]["av"] = av
            for loc, comp_d in all_dict.items():
                for comp, cnt in comp_d.items():
                    cav = comp_dict[comp]["av"]
                    availability = ["available"]
                    av = {
                        "available": cav["available"],
                        "exists": cav["exists"],
                        "needed": cnt,
                        "component": comp,
                        "location": loc
                    }
                    if av["available"]:
                        out["success"].append(av)
                    else:
                        out["failure"].append(av)    
        else:
            all_dict = self.get_ops_tuples_mult_in_one()
            for loc, comp_d in all_dict.items():
                for comp, cnt in comp_d.items():
                    av = get_availability_full(comp, cnt, loc)
                    if av["available"]:
                        out["success"].append(av)
                    else:
                        out["failure"].append(av)
        return out