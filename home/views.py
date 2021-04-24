from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView
from .forms import InternshipForm, ApplicationForm
from .models import Internship, InternshipApplication, Domains
import datetime, xlwt
from django.db.models import Q
from django.core.paginator import Paginator
import mimetypes


def home(request):
    return render(request, 'home/index.html')


def Internships(request, pg=1):
    internship = Internship.objects.all().order_by('-apply_by')

    query = request.GET.get("query")
    if query:
        internship = internship.filter(
            # Q(startup__icontains=query) |
            Q(field_of_internship__icontains=query) |
            Q(duration__icontains=query) |
            Q(about=query) |
            Q(location=query) |
            Q(stipend=query) |
            Q(skills_required=query) |
            Q(perks=query) 
            ).distinct()

    paginator = Paginator(internship, 100)

    context = {
        'Intern': paginator.page(pg),
        'page': pg,
      	'paginator': paginator,
        'internships': paginator.page(pg)
    }
    return render(request, 'home/internships.html', context)

def MyInternships(request):
    pg = 1
    if(request.user.is_authenticated):
        internships = Internship.objects.filter(internship__applied_by=request.user)
        context = {
            'internships': internships,
        }
        return render(request, 'home/MyInternship.html', context)
    else:
        redirect(internships, pg=pg)
    
    


def InternshipApplicationView(request, pk):
    pg = 1
    internship = Internship.objects.filter(id=pk).first()
    field = Domains.objects.filter(internship=internship)
    applied_by = InternshipApplication.objects.filter(applied_by=request.user)
    date = datetime.date.today()
    for applicant in applied_by:
        if(internship == applicant.internship):
            messages.success(request, f'You have already applied for this internship.')
            return redirect('internship-detail', pk)
    
    if(internship == None or date > internship.apply_by):
        messages.success(request, f'Applications for this internship is closed.')
        return redirect('internships', pg = pg)

    form = ApplicationForm(request.POST or None)


    if form.is_valid():
        form.instance.internship = Internship.objects.filter(id = pk).first()
        form.instance.applied_by = request.user
        form.instance.field = Domains.objects.filter(internship=internship)
        form.save()
        messages.success(request, f'You have successfully applied for this internship.')
        return redirect('internship-detail', pk)

    context = {
        'form': form,
        'internship':internship,
        'field':field,
    }
    return render(request, 'home/internship_application.html', context)



def InternshipDetailView(request, pk):
    pg = 1
    applied = False

    internship = Internship.objects.filter(id=pk).first()
    field = Domains.objects.filter(internship=internship)
    if(request.user.is_authenticated):
        applied_by = InternshipApplication.objects.filter(applied_by=request.user)
        for applicant in applied_by:
            if(internship == applicant.internship):
                applied = True
    
    context = {
        'object' : internship,
        'applied' : applied,
    }

    return render(request, 'home/internship_detail.html', context)






