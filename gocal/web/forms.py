"""
fiboweb forms
"""
from django import forms


class ExpressionForm(forms.Form):
    """ FibonacciForm """
    user_input = forms.CharField(
        label='Enter mathematical expression',
        label_suffix=': '
    )

