from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Member
from .forms import MemberForm

# Create your views here.
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
            
            member = Member(firstname=firstname, 
                            lastname=lastname,
                            phone=phone,
                            joined_date=joined_date)
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
