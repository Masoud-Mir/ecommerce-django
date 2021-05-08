from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView, PasswordResetView,
)

# Create your views here.
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from account.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from account.forms import SignUpForm, ProfileUpdateForm
from account.tokens import account_activation_token

UserModel = get_user_model()


class Login(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('shop:home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'فعالسازی حساب کاربری'
            message = render_to_string('registration/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/activation_confirm.html')
    else:
        form = SignUpForm()

    if request.user.is_authenticated:
        print(check_password('m1419844322', request.user.password))

    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return render(request, 'registration/activation_successful.html')
    else:
        return render(request, 'registration/activation_failed.html')


class ResetPass(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
#
#     def get_context_data(self, **kwargs):
#         current_password = self.request.user.password
#         form_class = PasswordResetForm
#
#         def form_valid(self, form):
#             opts = {
#                 'use_https': self.request.is_secure(),
#                 'token_generator': self.token_generator,
#                 'from_email': self.from_email,
#                 'email_template_name': self.email_template_name,
#                 'subject_template_name': self.subject_template_name,
#                 'request': self.request.user.,
#                 'html_email_template_name': self.html_email_template_name,
#                 'extra_email_context': self.extra_email_context,
#             }
#             form.save(**opts)
#             return super().form_valid(form)
#         is_old_pass = check_password()
#
#         context = super(ResetPass, self).get_context_data()
#         context


@login_required(login_url='login')
def profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'registration/profile.html', context=context)


@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
        else:
            ProfileUpdateForm(instance=user)
            return redirect('account:edit_profile')

    form = ProfileUpdateForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'registration/edit_profile.html', context=context)