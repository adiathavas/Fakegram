from django import forms
from .models import User

stringi = 's'

class LoginForm(forms.ModelForm):
    Login = forms.CharField(widget=forms.TextInput(
        attrs={
        'placeholder': 'IG Username',
            'color': '#333'
        }
    ))
    Password = forms.CharField(widget=forms.TextInput(
        attrs={
        'placeholder': 'IG Password ',
                       'color': '#fff',
            'font-size':'300%',
            'white-space': 'nowrap',
            'margin':'0 auto',
            'text-align': 'center',
            'clear': 'both',
            'float': 'left',
            'margin-right': '15px'


    }
    ))


    class Meta:
        model = User
        fields = ('Login', 'Password')

# class ActionForm(forms.ModelForm):
#     Analytics = forms.RadioSelect()
#     class Meta:
#         model = User
#         fields = ('Analytics')



class InputForm(forms.TextInput, forms.CharField):
    Input = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'placeholder': 'IG Password ',
            'color': '#000000',
            'font-size': '300%',
            'white-space': 'nowrap',
            'margin': '0 auto',
            'text-align': 'left',
            'clear': 'both',
            'float': 'left',
            'margin-right': '15px'
        }
    ))
    def get_data(self):
        return forms.CharField

