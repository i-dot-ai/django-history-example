from django import forms

from .models import Theme, Framework


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["name", "description"]


class FrameworkForm(forms.ModelForm):
    class Meta:
        model = Framework
        fields = ["name", "description"]


FrameworkFormSet = forms.modelformset_factory(
    Framework,
    form=FrameworkForm,
    extra=3
)
