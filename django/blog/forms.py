from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string

""" お問い合わせフォーム """
class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control contact rounded-0', 
                'placeholder': '名前',
            }
        ),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control contact rounded-0', 
                'placeholder': 'メールアドレス',
            }
        ),
    )
    subject = forms.CharField(
        label='',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control contact rounded-0', 
                'placeholder': '件名',
            }
        ),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control contact rounded-0', 
                'placeholder': '内容',
            }
        ),
    )

    def send_email(self):
        domain = Site.objects.get_current().domain
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER]
        context = {
            'domain': domain,
            'subject': subject,
            'message': message,
            'name': name,
            'email': email,
        }
        message = render_to_string('blog/mail.txt', context) 
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")