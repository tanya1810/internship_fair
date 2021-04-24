from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [

    path('', 						views.home,
         name='abcd'),
    path('internships/<int:pg>/', 						views.Internships,
         name='internships'),
     path('internships/', 						views.Internships,
         name='home'),
     path('my-internships/',                     views.MyInternships,
         name='my-internships'),
    path('internships/<int:pk>/details',
         views.InternshipDetailView,             name='internship-detail'),
    path('internships/<int:pk>/application/',
         views.InternshipApplicationView,        name='internship-application'),
     path('download/<int:pk>/',                  views.exceldownload,
         name='excel-download'),
]
