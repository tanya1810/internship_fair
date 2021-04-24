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

    print(form.is_valid())
    print(form.errors)

    if form.is_valid():
        u=request.user
        if(u.count>=10):
            messages.success(request, f'You have already applied for 10 internships. You can check for the companies you have applied for in the My-Internships section.')
            return redirect('internships', pg = pg)
        form.instance.internship = Internship.objects.filter(id = pk).first()
        form.instance.applied_by = request.user
        # form.instance.field = Domains.objects.filter(internship=internship)
        u.count+=1
        u.save()
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
        'field': field,
    }

    return render(request, 'home/internship_detail.html', context)


def exceldownload(request, pk = None):
    internship = Internship.objects.filter(id=pk).first()
    if request.user.is_authenticated: 
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Internship Applications.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(internship.domain) # this will make a sheet named Users Data

        row_num = 0

        style = 'font: bold 1; border: top thick, right thick, bottom thick, left thick;'
        font_style = xlwt.easyxf(style)
        columns = ['Resume', 'Name', 'E-mail', 'Contact No.']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

        styles = [
            'align: wrap 1; border: left thick, right thick;',
            'font: underline 1;',
            'align: horiz center; border: left thick, right thick;',
            'border: left thick, right thick;',
       ]

        rows = InternshipApplication.objects.filter(id=pk).values_list('resume', 'applied_by__name', 'applied_by__email', 'applied_by__contact')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                if col_num == 0:
                    font_style = xlwt.easyxf(styles[0])
                elif col_num == 1:
                    font_style = xlwt.easyxf(styles[1])
                elif col_num == 5 or col_num == 6:
                    font_style = xlwt.easyxf(styles[2])
                else:
                    font_style = xlwt.easyxf(styles[3])

                if col_num == 1:
                    ws.write(row_num, col_num, xlwt.Formula('HYPERLINK("%s")'%row[col_num]), font_style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)

        font_style = xlwt.easyxf('border: top thick;')
        row_num += 1
        for col_num in range(len(columns)):  
            ws.write(row_num, col_num, "", font_style)

        ws.col(0).width = 256*27
        ws.col(1).width = 256*20
        ws.col(2).width = 256*20
        ws.col(3).width = 256*30
        ws.col(4).width = 256*25
        ws.col(5).width = 256*15
        ws.col(6).width = 256*15
        ws.col(7).width = 256*20
        ws.col(8).width = 256*20

        wb.save(response)

        return response

    else:
        messages.success(request, f'You are not authorised to access this data.')
        return redirect('abcd')






