from django.db import models
from django.urls import reverse
from user.models import User
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

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

    def __str__(self):
        return self.company_name + "(" + str(self.id) + ")"

    def get_absolute_url(self):
        return reverse('internship-detail', kwargs={'pk' : self.pk})

    def about_markdown(self):
        about = self.about
        return mark_safe(markdown(about))

    def get_next_post(self):
        next_post = self.get_previous_by_apply_by()
        if next_post:
        	return next_post
        return False   	

    def get_prev_post(self):
        prev_post = self.get_next_by_apply_by()
        if prev_post:
        	return prev_post
        return False

class InternshipApplication(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, default='', related_name='internship')
    applied_by = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='intern')
    
    def __str__(self):
        return self.internship.company_name + "(" + str(self.internship.id) + ")" + " - " + self.applied_by.name

    def message_markdown(self):
        message = self.message
        return mark_safe(markdown(message))