from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.permissions import AllowAny
from django import forms

from .serializers import RegisterSerializer, LoginSerializer
from .models import User

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,  force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .forms import RegistrationForm
from .utils import email_verification_token
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth import login
from django.views import View
from django.core.mail import EmailMessage
# class RegisterView(generics.CreateAPIView):
#     """
#     The API View for user registration
#     """

#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer


class RegisterView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'email/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until it is confirmed
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'email/confirmation_sent.html')
        return render(request, 'email/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'email/activation_email.html')

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # Deactivate account until email confirmed
#             user.save()

#             current_site = get_current_site(request)
#             subject = 'Activate Your Account'
#             message = render_to_string('registration/activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': email_verification_token.make_token(user),
#             })
#             send_mail(subject, message, 'your_email@example.com', [user.email])
#             return render(request, 'registration/registration_pending.html')
#     else:
#         form = RegistrationForm()
#     return render(request, 'registration/register.html', {'form': form})


# def activate_account(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and email_verification_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return redirect('home')  # Redirect to the home page or dashboard
#     else:
#         return HttpResponse('Activation link is invalid!')


class LoginView(generics.GenericAPIView):
    """
    The API View for user login.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handles the HTTP POST request for user login
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
