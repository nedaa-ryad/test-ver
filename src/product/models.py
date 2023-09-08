from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

CATEGORY_CHOICES = (
    ('BE', 'Bed'),
    ('SO', 'Sofa'),
    ('CH', 'Chair'),
    ('LI', 'Lighting'),
    ('TA', 'Table'),
    ('DT', 'Dining_Table'),
) 

class Product(models.Model):
    title = models.CharField(verbose_name=_("Product_Title"), max_length=50)
    description = models.TextField(verbose_name=_("Description"))
    category = models.CharField(choices= CATEGORY_CHOICES, max_length=2, verbose_name=_("Category"))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Product_Price"))
    discountPrice = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Product_Discount Price"), blank=True, null=True)
    image = models.ImageField(verbose_name=_("Product Image"), upload_to='Product')
    created = models.DateTimeField(verbose_name=_("Product_Created At"))
    isNew = models.BooleanField(
        verbose_name=_("New Product"), default=True)
    isBestSeller = models.BooleanField(
        verbose_name=_("Best Seller"), default=False)

    slug = models.SlugField(
        blank=True, null=True, verbose_name=_('Product_URL'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_related_products(self):
        related_products = Product.objects.filter(category=self.category).exclude(pk=self.pk)[:4]
        return related_products

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(verbose_name=_("Images"), upload_to='Product')

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return self.product.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 150)
    locality = models.CharField(max_length = 150)
    city = models.CharField(max_length = 100)
    mobile = models.IntegerField(default=0)
    zipCode = models.IntegerField()


    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_(
        "product"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_("quantity"), default=1)
    price_id = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Stripe Price ID"))

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
    
    @property
    def total_cost(self):
        if self.product.discountPrice is not None:
            return self.quantity * self.product.discountPrice
        else:
            return self.quantity * self.product.price

class Wishlist(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_(
        "product"), on_delete=models.CASCADE)
