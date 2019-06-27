from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        models = User
        fields = ('full_name','email',)
        
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("password don't match.")
        return password2
    
    def save(self,commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name','email','password','active','admin',)
    
    def clean_password(self):
        return self.initial['password']



class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=255,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}), label='Confirm Passsword.')
    full_name = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    
    class Meta:
        model = User
        fields = ('full_name','email',)
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('E-mail is taken.')
        return email
    
    def clean(self):
        data = self.cleaned_data
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Password must match.')
        return data
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user