from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Member
from .forms import MemberForm, LoginForm, RegistroForm

#decorador validador de rutas:
def requiere_usuario(tipo_requerido):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if 'usuario_tipousuario' not in request.session or request.session['usuario_tipousuario'] != tipo_requerido:
                return redirect('main')
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

# Create your views here.
import requests
def main(request):
    respuesta = requests.get('https://mindicador.cl/api')
    dolar = respuesta.json()['dolar']['valor']
    return render(request, 'index.html', {'request': request, 'dolar': dolar})

def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {'mymembers': mymembers}
    return HttpResponse( template.render(context,request) )

def details(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {'mymember': mymember}
    return HttpResponse(template.render(context, request))

@requiere_usuario('admin')
def crear_miembro(request):
    template = loader.get_template("formulario-miembros.html")
    if request.method == 'GET':
        form = MemberForm(request.GET)
        if form.is_valid():
            #rescatando los datos
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            phone = form.cleaned_data['phone']
            joined_date = form.cleaned_data['joined_date']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            repeat_pass = form.cleaned_data['repeat_password']
            tipo_usuario = form.cleaned_data['tipo_usuario']
            if password!=repeat_pass:
                #debería enviar una alerta de error de contraseñas: misión de ustedes:
                form = MemberForm()
                context = {'form': form}
                return HttpResponse(template.render(context, request))
            else:
                member = Member(firstname=firstname, 
                                lastname=lastname,
                                phone=phone,
                                joined_date=joined_date,
                                email=email,
                                password=repeat_pass,
                                tipo_usuario=tipo_usuario)
                member.save()
                return redirect('members')
        else:
            form = MemberForm()
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        form = MemberForm()
        context = {'form': form}
        return HttpResponse( template.render(context, request) )

def login(request):
    template = loader.get_template('login.html')
    form = LoginForm()
    context = {'form': form}
    if request.method=='GET':
        form = LoginForm(request.GET)
        if form.is_valid():
            try:
                correo = form.cleaned_data['email']
                clave = form.cleaned_data['password']
                usuario_logueado = Member.objects.get(email=correo, password=clave)
                request.session['usuario_id'] = usuario_logueado.id
                request.session['usuario_tipousuario'] = usuario_logueado.tipo_usuario
                request.session['usuario_firstname'] = usuario_logueado.firstname
                return redirect('main')
            except:
                #aquí deberian mostrar un mensaje de error:
                pass
    return HttpResponse(template.render(context, request))

def logout(request):
    request.session.flush()
    return redirect('main')

def registro(request):
    template = loader.get_template("registro.html")
    if request.method == 'GET':
        form = RegistroForm(request.GET)
        if form.is_valid():
            #rescatando los datos
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            phone = form.cleaned_data['phone']
            joined_date = form.cleaned_data['joined_date']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            repeat_pass = form.cleaned_data['repeat_password']
            tipo_usuario = "jugador"
            if password!=repeat_pass:
                #debería enviar una alerta de error de contraseñas: misión de ustedes:
                form = RegistroForm()
                context = {'form': form}
                return HttpResponse(template.render(context, request))
            else:
                member = Member(firstname=firstname, 
                                lastname=lastname,
                                phone=phone,
                                joined_date=joined_date,
                                email=email,
                                password=repeat_pass,
                                tipo_usuario=tipo_usuario)
                member.save()
                return redirect('login')
        else:
            form = RegistroForm()
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        form = RegistroForm()
        context = {'form': form}
        return HttpResponse( template.render(context, request) )

