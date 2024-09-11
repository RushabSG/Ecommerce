from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class Category(models.Model):

    name = models.CharField(
        max_length=250, db_index=True
    )  # query acceleration and faster lookup
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    """
    change display name for object 
    i.e., Shoes, Jackets, etc.
    """

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("list_category", args=[self.slug])


class Product(models.Model):
    # Foreign key
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default="un-branded")
    description = models.TextField(
        blank=True
    )  # blank=true means optional while filling the form
    slug = models.SlugField(max_length=250)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    images = models.ImageField(upload_to="images", null=True)

    class Meta:
        verbose_name_plural = "products"

    """
    change display name for object name
    i.e., Nike_jordan_shoes, etc. to avoid object_1 as name in DB
    """

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_info", args=[self.slug])
