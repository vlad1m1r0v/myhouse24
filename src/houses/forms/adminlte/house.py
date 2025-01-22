from django import forms

from src.houses.models import House


class AdminHouseForm(forms.ModelForm):
    name = forms.CharField(
        label='Назва',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'minlength': 5,
                'maxlength': 30
            }
        )
    )

    address = forms.CharField(
        label='Адреса',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'minlength': 10,
                'maxlength': 60
            }
        )
    )

    image_1 = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення #1. Рекомендований розмір: (522x350)')

    image_2 = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення #2. Рекомендований розмір: (248x160)')

    image_3 = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення #3. Рекомендований розмір: (248x160)')

    image_4 = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення #4. Рекомендований розмір: (248x160)')

    image_5 = forms.ImageField(
        widget=forms.FileInput(),
        label='Зображення #5. Рекомендований розмір: (248x160)')

    class Meta:
        model = House
        fields = '__all__'