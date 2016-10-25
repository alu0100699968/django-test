from django.views import generic
# porque el modelo User se llama igual xd
from django.contrib.auth.models import User as DUser
from django.contrib.auth.models import Group
from django.contrib.auth import login

from .models import User
from . import forms

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'users/index.html'

class ListUsersView(generic.ListView):
    template_name = 'users/list_users.html'
    model = User

class DetailView(generic.DetailView):
    model = User

    # se sobreescribe para pasar como contexto al template la variable is_staff
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        #context.update({'is_staff': self.request.user.groups.filter(name='staff').exists()})
        context['is_staff'] = self.request.user.groups.filter(name='staff').exists()
        context['is_solicitante'] = self.request.user.groups.filter(name='solicitante').exists()
        return context

class EditView(generic.UpdateView):
    model = User
    template_name = 'users/edit_view.html'
    fields = ['estado', 'centro_asignado', 'horario_asignado']

class UserRegister(generic.edit.CreateView):
    model = User
    form_class = forms.UserRegisterForm
    #fields = ['nombre', 'apellido1', 'apellido2', 'dni', 'titulacion', 'email', 'telefono']

    def form_valid(self, form):
        user = form.save()
        new_user = DUser.objects.create_user(user.dni, user.email,
            form.cleaned_data.get('password1'), first_name=user.nombre,
            last_name=user.apellido1 + ' ' + user.apellido2)
        g = Group.objects.get(name='solicitante')
        g.user_set.add(new_user)
        login(self.request, new_user)
        return super(UserRegister, self).form_valid(form)
