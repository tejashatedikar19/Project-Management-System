from django.db import models
from django.conf import settings

class Tag(models.Model):
    tag = models.CharField(max_length=50)
    def __str__(self):
        return self.tag
    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ['tag']

class Group(models.Model):
    sname = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    dept = models.CharField(max_length=60)
    academic_year = models.CharField(max_length=10, default=settings.CURR_YEAR)
    registered_semester = models.IntegerField(default=settings.CURR_SEM)
    div = models.CharField(max_length=10)
    prn = models.BigIntegerField()
    roll = models.BigIntegerField()
    contact_num = models.FloatField()
    group_id = models.CharField(max_length=8, primary_key=True)
    memName1 = models.CharField(max_length=30, default='Name of the member', blank=True)
    memPRN1 = models.BigIntegerField(default=0)
    memRoll1 = models.BigIntegerField(default=0)
    memEmail1 = models.EmailField(max_length=30, blank=True)
    memName2 = models.CharField(max_length=30, default='Name of the member', blank=True)
    memPRN2 = models.BigIntegerField(default=0)
    memRoll2 = models.BigIntegerField(default=0)
    memEmail2 = models.EmailField(max_length=30, blank=True)
    memName3 = models.CharField(max_length=30, default='Name of the member', blank=True)
    memPRN3 = models.BigIntegerField(default=0)
    memRoll3 = models.BigIntegerField(default=0)
    memEmail3 = models.EmailField(max_length=30, blank=True)
    pname = models.CharField(max_length=100, default='Name of the project')
    guide = models.CharField(max_length=40, default='Guide of the project')
    domain = models.CharField(max_length=50, default='Domain of the project')
    description = models.TextField(default='Description of the project')
    # tags = models.ManyToManyField(Tag)
    tags = models.CharField(max_length=150, default='Tags of the project')
    submitted_PS = models.BooleanField(default=False)
    midsem_conducted = models.BooleanField(default=False)
    endsem_conducted = models.BooleanField(default=False)
    PPT = models.FileField(upload_to='PPT/', blank=True)
    working_model = models.FileField(upload_to='WorkingModel/', blank=True)
    report = models.FileField(upload_to='Report/', blank=True)
    grade = models.CharField(max_length=2, default='NA')
    remarks = models.TextField(default='', blank=True)
    requested_guide = models.CharField(max_length=40, default='NA')
    guide_approved = models.IntegerField(default=0)
    def _str_(self):
        return self.sname
    class Meta:
        verbose_name_plural = 'Groups'
        ordering = ['sname']

class Faculty(models.Model):
    fname = models.CharField(max_length=40)
    email = models.EmailField(max_length=30, primary_key=True)
    dept = models.CharField(max_length=60)
    registered_academic_year = models.CharField(max_length=30, default=settings.CURR_YEAR)
    registered_semester = models.IntegerField(default=settings.CURR_SEM)
    contact_num = models.FloatField()
    qualification = models.CharField(max_length=150, default='')
    joining_date = models.DateField(default='2020-01-01')
    group_requests = models.TextField(default='')
    def __str__(self):
        return self.fname
    class Meta:
        verbose_name_plural = 'Faculties'
        ordering = ['fname']

class Coordinator(models.Model):
    cname = models.CharField(max_length=40)
    email = models.EmailField(max_length=30, primary_key=True)
    dept = models.CharField(max_length=60)
    registered_academic_year = models.CharField(max_length=30, default=settings.CURR_YEAR)
    registered_semester = models.IntegerField(default=settings.CURR_SEM)
    contact_num = models.FloatField()
    def __str__(self):
        return self.cname
    class Meta:
        verbose_name_plural = 'Coordinators'
        ordering = ['cname']
