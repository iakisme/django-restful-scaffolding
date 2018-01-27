from django.contrib.auth import get_user_model
from django.db import models
import uuid

# Create your models here.

from common.models import CoreModel


def scramble_uploaded_filename(instance, filename):
    """
    Scramble / uglify the filename of the uploaded file, but keep the files extension (e.g., .jpg or .png)
    :param instance:
    :param filename:
    :return:
    """
    extension = filename.split(".")[-1]
    return "static/photos/{}.{}".format(uuid.uuid4(), extension)


class Dream(CoreModel):
    # image = models.ImageField(upload_to=scramble_uploaded_filename, null=True, blank=True, max_length=255,default='default')
    image_url = models.CharField(max_length=1000, blank=True, null=True, default='static/photos/default_img.jpg')

    title = models.CharField(max_length=1000, blank=True, null=True)
    person_name = models.CharField(max_length=100, blank=True, null=True)
    # age = models.IntegerField(null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    # person_type = models.CharField(max_length=100, blank=True, null=True)
    reason = models.CharField(max_length=1000, blank=True, null=True)
    local = models.CharField(max_length=100, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=100, blank=True, null=True)

    # contact_person = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE)
    is_claimed = models.BooleanField(default=False)
    donor = models.ManyToManyField('Donor', null=True, blank=True)

    class Meta:
        ordering = ('-is_claimed', '-created_at',)


class Donor(CoreModel):
    name = models.CharField(max_length=1000, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
