from django.db import models
from django.urls import reverse
from user.models import User
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

class Domains(models.Model):
    domain = models.CharField(max_length=50)

    def __str__(self):
        return self.domain
        

class Internship(models.Model):
    company_name = models.CharField(max_length=100, default='')
    company_logo = models.ImageField(default='logo/download.png', upload_to='logo/')
    start_by = models.DateField(default='2000-01-01', help_text='YYYY-MM-DD Format should be followed for the date.')
    field_of_internship = models.CharField(max_length=100, default='')
    duration = models.CharField(max_length=20)
    about = models.TextField()
    location = models.CharField(max_length=100)
    stipend = models.CharField(max_length=100)
    skills_required = models.CharField(max_length=500)
    no_of_internships = models.PositiveIntegerField()
    perks = models.CharField(max_length=100)
    apply_by = models.DateField(default='2000-01-01', help_text='YYYY-MM-DD Format should be followed for the date.')

    who_should_apply = models.CharField(max_length=200)

    domain = models.ManyToManyField(Domains)

    def __str__(self):
        return self.company_name + "(" + str(self.id) + ")"


class InternshipApplication(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, default='', related_name='internship')
    applied_by = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='intern')

    domain = models.ManyToManyField(Domains)

    
    def __str__(self):
        return self.internship.company_name + "(" + str(self.internship.id) + ")" + " - " + self.applied_by.name

