from django.contrib import admin
from .models import Internship, InternshipApplication, Domains

admin.site.register(Internship)
admin.site.register(InternshipApplication)
admin.site.register(Domains)