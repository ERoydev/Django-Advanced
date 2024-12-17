from django import forms
import time

class DisableFieldsMixin(forms.Form):
    disabled_fields = ()
    # Taka moga perizpolzvam logikata v formite
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name in self.disabled_fields:
                self.fields[field].disabled = True

