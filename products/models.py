import random
import os
from django.db import models


def get_filename_extensions(filename):
    base_name = os.path.basename(filename)
    name, extension = os.path.splitext(base_name)
    return name, extension


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 4654654)
    name, extension = get_filename_extensions(filename)
    final_filename = '{new_filename}{extension}'.format(
                                                new_filename=new_filename,
                                                extension=extension
                                            )
    return 'products/{new_filename}/{final_filename}'.format(
                                                    final_filename=final_filename,
                                                    new_filename=new_filename
                                                )


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
