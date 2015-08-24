from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User
from forms import RegistrationForm
from datetime import datetime


@login_required(redirect_field_name=None)
def index(request):
    visits = int(request.COOKIES.get('visits', '1'))

    reset_last_visit_time = False
    response = render(request, 'AuthenticationApp/index.html', {'user': request.user, 'visits': visits})
    # Does the cookie last_visit exist?
    if 'last_visit' in request.COOKIES:
        # Yes it does! Get the cookie's value.
        last_visit = request.COOKIES['last_visit']
        # Cast the value to a Python date/time object.
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        # If it's been more than a day since the last visit...
        if (datetime.now() - last_visit_time).seconds > 5:
            visits = visits + 1
            # ...and flag that the cookie last visit needs to be updated
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so flag that it should be set.
        reset_last_visit_time = True

        #Obtain our Response object early so we can add cookie information.
        response = render(request, 'AuthenticationApp/index.html', {'user': request.user, 'visits': visits})

    if reset_last_visit_time:
        response.set_cookie('last_visit', datetime.now())
        response.set_cookie('visits', visits)

    # Return response back to the user, updating any cookies that need changed.
    return response


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return render(request, 'AuthenticationApp/success.html', )
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'AuthenticationApp/signup.html',
        variables,
    )


def validate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return index(request)
        else:
            return render(request, 'AuthenticationApp/login.html', {'user': user,
                                                                    'error_message': "Your account has been disabled.",
            })

    else:
        return render(request, 'AuthenticationApp/login.html', {'user': user,
                                                                'error_message': "Username and Password are incorrect.",
        })


def register_success(request):
    return render(request, 'AuthenticationApp/success.html')


def user_login(request):
    return render(request, 'AuthenticationApp/login.html')


def user_logout(request):
    logout(request)
    return render(request, 'AuthenticationApp/login.html')


def profile_success(request):
    return render(request, 'AuthenticationApp/profile_success.html')


def edit_user_profile(request):
    # data = {'username': request.user.username, 'email': request.user.email, 'password': request.user.password,
    # 'first_name': request.user.first_name, 'last_name': request.user.last_name}
    if request.method == "POST":
        pform = RegistrationForm(data=request.POST, instance=request.user)
        if pform.is_valid():
            user = pform.save(commit=False)
            user.set_password(pform.cleaned_data['password'])
            user.save()
        return profile_success(request)
    else:
        form = RegistrationForm(
            instance=request.user)  # bound data and initial= data--- unbound data and no validation no error..

    return render(request, 'AuthenticationApp/edit_user_profile.html',
                  {'form': form}
    )