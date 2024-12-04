from django import forms

from .models import FrameworkTheme, Theme


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["name", "description"]


class FrameworkForm(forms.ModelForm):
    class Meta:
        model = FrameworkTheme
        fields = ["name", "description"]


FrameworkFormSet = forms.modelformset_factory(FrameworkTheme, form=FrameworkForm, extra=3)
