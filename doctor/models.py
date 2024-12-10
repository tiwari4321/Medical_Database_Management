from django.db import models
from account.models import *
import os 
import uuid
# Create your models here.

TypeofBlooadGroup = (
    ("A+","A+"),
    ("A-","A-"),
    ("B+","B+"),
    ("B-","B-"),
    ("AB+","AB+"),
    ("AB-","AB-"),
    ("O+","O+"),
    ("O-","O-"),
)

class ResearcherProfile(models.Model):
    GENDER = (('M','MALE'),('F','FEMALE'))
    researcher = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(default='M',choices=GENDER, max_length=1)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10,null=True)
    dob = models.DateField()
    otp = models.CharField(max_length=5,null=True,blank=True)
    verified_phone = models.BooleanField(default=False,null=True)
    organization = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255,null=True)
    country_code = models.CharField(max_length=2, default="91")
    id_image = models.ImageField(upload_to='researcherprofile',default="")

    def __str__(self):
        return self.first_name

class DoctorProfile(models.Model):
    GENDER = (('M','MALE'),('F','FEMALE'))
    doctor = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(default='M',choices=GENDER, max_length=1)
    otp = models.CharField(max_length=5,null=True,blank=True)
    verified_phone = models.BooleanField(default=False,null=True)
    first_name = models.CharField(max_length=255)
    license_key = models.CharField(max_length=255)
    verified_admin = models.BooleanField(default=False,null=True)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10,null=True)
    dob = models.DateField()
    specialization = models.CharField(max_length=255,null=True)
    country_code = models.CharField(max_length=2, default="91")

    def __str__(self):
        return self.first_name

class PatientProfile(models.Model):
    GENDER = (('M','MALE'),('F','FEMALE'))
    added_by = models.ForeignKey(User,on_delete=models.CASCADE)
    gender = models.CharField(default='M',choices=GENDER, max_length=1)
    first_name = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=3,choices=TypeofBlooadGroup,default='A+')
    hospital = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.IntegerField()
    dob = models.DateField()

    def __str__(self):
        return self.first_name


def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = "%s.%s" % (uuid.uuid4(), ext)
        # filename= instance.name + instance.modality + uuid.uuid4()
    return os.path.join(
      "%s" % instance.name, "%s" % instance.modality, filename)

Possibility = (
("YES", "YES"),
("NO", "NO"),
)

TypeofModality = (
    ("X-ray","X-ray"),
    ("CT-scan","CT-scan"),
    ("MRI","MRI"),
    ("UltraSound","Ultrasound"),
    ("Angiography","Angiography"),
    ("Electrocardiogram","ECG"),
    ("PET","PET"),
    ("OCT","OCT")
)



MEDIA_CHOICES = [
    ('Audio', (
            ('vinyl', 'Vinyl'),
            ('cd', 'CD'),
        )
    ),
    ('Video', (
            ('vhs', 'VHS Tape'),
            ('dvd', 'DVD'),
        )
    ),
    ('unknown', 'Unknown'),
]

class DiseaseDetails(models.Model):
    patient = models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=True)
    organ = models.CharField(max_length=100,null=True)
    modality=models.CharField(max_length=30,choices=TypeofModality,default='X-ray')
    diagonised = models.CharField(max_length = 20, choices = Possibility, default = 'YES')
    img=models.ImageField(upload_to=get_upload_path,null=True)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

