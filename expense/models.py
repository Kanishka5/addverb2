from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

PROFILE_CHOICES = (("1", "Manager"), ("2", "Engineer"), ("3", "Accountant"))


# employee table ->
class Employee(AbstractUser):
    username = models.CharField(blank=False, max_length=20,
                                unique=True)  #employee id
    name = models.CharField(blank=False, max_length=50, default='admin')
    accountno = models.CharField(blank=False, max_length=30, default='00000')
    email = models.EmailField(blank=False)
    profile = models.CharField(max_length=20,
                               choices=PROFILE_CHOICES,
                               default='2')
    mobile = models.CharField(blank=False, max_length=10, default="0000000000")
    managerid = models.ForeignKey('Employee',
                                  blank=True,
                                  null=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return self.username

    def publish(self):
        self.save()


#expense table ->
class Expense(models.Model):
    amount = models.FloatField(blank=False)
    description = models.CharField(blank=False, max_length=100)
    date = models.DateField(blank=False)
    attachments = models.FileField(blank=False, upload_to='attachments/')
    approvalstatus = models.BooleanField(default=False)
    paymentstatus = models.BooleanField(default=False)
    username = models.ForeignKey(Employee,
                                 blank=False,
                                 on_delete=models.CASCADE) #employeeid

    def __str__(self):
        return self.description

    def publish(self):
        self.save()
