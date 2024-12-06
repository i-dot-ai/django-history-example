from django import forms

from .models import FrameworkTheme, ResponseMapping, Theme


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["name", "description"]


class FrameworkForm(forms.ModelForm):
    class Meta:
        model = FrameworkTheme
        fields = ["name", "description"]


class ResponseMappingForm(forms.ModelForm):
    response_text = forms.CharField(
        label="Response Text", required=False, widget=forms.Textarea(attrs={"readonly": "readonly"})
    )

    class Meta:
        model = ResponseMapping
        fields = ["response_text", "framework_theme"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["response_text"].initial = self.instance.response.response


FrameworkFormSet = forms.modelformset_factory(FrameworkTheme, form=FrameworkForm, extra=3)
