from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Classroom(models.Model):
	name = models.CharField(max_length=120)
	subject = models.CharField(max_length=120)
	year = models.IntegerField()
	teacher = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('classroom-detail', kwargs={'classroom_id':self.id})


class Student(models.Model):
	name = models.CharField(max_length=120)
	date_of_birth = models.DateField()
	GENDER_CHOICES = (
	('MALE', 'Male'),
	('FEMALE', 'Female'),
    )
	gender = models.CharField(
        max_length=8,
        choices=GENDER_CHOICES,
    )
	exam_grade = models.DecimalField(decimal_places=3,max_digits=7)
	classroom = models.ForeignKey(Classroom,  on_delete=models.CASCADE,  null=True, blank=True)
