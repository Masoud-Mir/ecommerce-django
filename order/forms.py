from django import forms
from django.forms import ModelForm

from products.models import Product


# class ShoppingCartForm(forms.Form):
#
#     product_id = forms.IntegerField(
#         widget=forms.HiddenInput(),
#     )
#     amount = forms.IntegerField(
#         widget=forms.NumberInput(attrs={'min': 1, 'default': 1}),
#         initial=1
#     )

    # COLOR_CHOICE = Product.objects.get(id=product_id).color.all()
    # SIZE_CHOICE = Product.objects.get(id=product_id).size.all()
    #
    # color = forms.ChoiceField(
    #     choices=COLOR_CHOICE,
    #     widget=forms.RadioSelect(),
    # )
    # size = forms.CharField(
    #     choices=SIZE_CHOICE,
    #     widget=forms.RadioSelect(),
    # )


class ShoppingCartForm(ModelForm):

    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1, 'default': 1}),
        initial=1
    )

    class Meta:
        model = Product
        fields = ['color', 'size']
