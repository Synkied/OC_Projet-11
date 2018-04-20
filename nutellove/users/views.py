from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View
from nutellove.forms import UserForm


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    # display blank form
    def get(self, request):  # pragma: no cover
        # initiate a form without data (None)
        form = self.form_class(None)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    # process data form
    def post(self, request):
        form = self.form_class(request.POST)
        context = {
            'form': form,
        }

        if form.is_valid():
            # raw data
            user = form.save(commit=False)

            # clean (normalized) data
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user.set_password(raw_password)
            user.save()

            # returns User object if credentials are correct
            user = authenticate(username=username, password=raw_password)

            if user is not None:
                # check if user is active
                if user.is_active:
                    login(request, user)
                    return redirect('index')

        # else: try again
        return render(request, self.template_name, context)  # paragm: no cover


class UserAccountView(LoginRequiredMixin, View):
    template_name = 'account.html'

    def get(self, request):
        # get the current logged in user
        current_user = request.user

        context = {
            'user': current_user,
        }

        return render(request, self.template_name, context)


class UserChangePassword(LoginRequiredMixin, View):

    template_name = 'users/change_password.html'

    def get(self, request):  # pragma: no cover
        # empty form for the connected user
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        # filled form sent to POST
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            # updates the session so the user doesn't have to reconnect
            # after changing password
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Votre mot de passe a été modifié avec succès !'
            )
            # return to the account page
            return redirect('users:account')

        else:
            messages.error(
                request, 'Un souci est survenu lors du changement \
                de mot de passe, assurez vous de bien entrer deux fois le même mot de passe.'
            )

            # if incorrect inputs, reload the page
            form = PasswordChangeForm(request.user)
            return render(request, self.template_name, {
                'form': form
            })
