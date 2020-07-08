from django import forms
from .choices import ActionCQChoices, ExpertCQChoices, PopularCQChoices
from .models import Argument, ActionScheme, ExpertOpinionScheme, PopularOpinionScheme

class ArgumentForm(forms.ModelForm):

    class Meta:
        model = Argument
        fields = ['target_critical_question', 'scheme_type']

    def __init__(self, pk=None, *args, **kwargs):
        parent_argument = Argument.objects.get(id=pk)
        super(ArgumentForm, self).__init__(*args, **kwargs)
        if parent_argument.scheme_type == 'action':
            self.fields['target_critical_question'].widget = forms.Select(choices=ActionCQChoices.choices)
        elif parent_argument.scheme_type == 'expert':
            self.fields['target_critical_question'].widget = forms.Select(choices=ExpertCQChoices.choices)
        elif parent_argument.scheme_type == 'popular':
            self.fields['target_critical_question'].widget = forms.Select(choices=PopularCQChoices.choices)

class ActionSchemeForm(forms.ModelForm):

    class Meta:
        model = ActionScheme
        fields = ['situation', 'action','goal','value']

class ExpertOpinionSchemeForm(forms.ModelForm):

    class Meta:
        model = ExpertOpinionScheme
        fields = ['domain','expert_source','assertion','reference']

class PopularOpinionSchemeForm(forms.ModelForm):

    class Meta:
        model = PopularOpinionScheme
        fields = ['assertion', 'reference']
