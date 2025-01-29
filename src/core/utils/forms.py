from django import forms
from django.core.exceptions import ValidationError


class AJAXModelChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            model = self.queryset.model
            value = model.objects.get(**{key: value})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise ValidationError("Вибране значення не знайдено в базі даних")
        return value
