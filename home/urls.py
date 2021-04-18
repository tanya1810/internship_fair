from django.urls import path
from . import views


urlpatterns = [

    path('internships/<int:pg>/', 						views.Internships,						name='internships'),	
    path('internships/', 								views.Internships,						name='home'),
    path('internships/<int:pk>/details', 				views.InternshipDetailView,				name='internship-detail'),
    path('internships/<int:pk>/application/', 			views.InternshipApplicationView,        name='internship-application'),
]
