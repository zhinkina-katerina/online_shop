from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.shortcuts import reverse

from .utils import unique_slug_generator, upload_image_path


class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()

    def with_id_in(self, ids):
        return self.filter(id__in=ids)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def get_active(self):
        return self.get_queryset().active()

    def features(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        queryset = self.get_queryset().filter(id=id)
        if queryset.count() == 1:
            return queryset.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

    def get_products_with_id_in(self, list_id):
        return self.get_queryset().with_id_in(list_id)

    def get_products_with_quantity_and_total(self, dict_with_quantity):
        products = self.get_queryset().with_id_in(dict_with_quantity.keys())
        for item in products:
            item.quantity = dict_with_quantity[str(item.id)]
        total = sum([item.price * int(item.quantity) for item in products])
        return products, total


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})


def product_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_reciever, sender=Product)
