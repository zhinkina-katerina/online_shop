import os
import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


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
