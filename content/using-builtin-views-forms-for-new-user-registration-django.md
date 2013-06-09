Title: Using the built-in views and forms for new user registration in Django
Date: 2013-06-09 01:10
Tags: django, authentication 
Author: Harry
Summary: I think Django gives you everything you need for a new user registration form in about 2 lines of urls.py config... am i right?

Have been digging into the built-in forms and views from
django.contrib.auth.  I always knew you could get generic views for login,
logout, even password reset, but I didn't know you could actually handle
new user creation as well!

There's a form in `django.contrib.auth.forms`, and a class-based view for
creating new objects called `CreateView`, and I believe this is all you
need for a working registration form/view:

    from django.views.generic.edit import CreateView
    from django.contrib.auth.forms import UserCreationForm

    urlpatterns = patterns('',
        url('^register/', CreateView.as_view(
                template_name='register.html',
                form_class=UserCreationForm,
                success_url='/'
        )),
        url('^accounts/', include('django.contrib.auth.urls')),

        # rest of your URLs as normal
    )

Then, in *register.html*, you get a `{{ form }}` you can use, including
a username, password and password confirmation, and it handles validation
errors and EVERYTHING.

Obviously it doesn't include registering (and validating) an email address 
for the user, but still, I'm pretty excited.  Did everyone else already
know about this?


