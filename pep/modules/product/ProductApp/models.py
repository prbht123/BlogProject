from django.db import models
import uuid
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from modules.models import BaseModel, AddressModel


class CategoryModel(BaseModel):
    """
    Category model for products
    """
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    # Function to return unique slug
    def unique_slug(self):
        unique_slugg = slugify(self.title)
        num = 1
        while CategoryModel.objects.filter(slug=unique_slugg).exists():
            unique_slugg = "{}-{}".format(unique_slugg, num)
            num += 1
            break
        return unique_slugg

    # Slugify Function
    def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = self.unique_slug()
      return super().save(*args, **kwargs)

    # Function to return name on table
    def __str__(self):
        return self.title


class TagModel(models.Model):
    """
        TagBlog model for tags of products
    """
    name = models.CharField(max_length=50, unique=True)

    # Function to return name on table
    def __str__(self):
        return self.name


class ProductModel(BaseModel, AddressModel):
    """
    Product Model to create product table
    """
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(CategoryModel, related_name='productmodel_category',on_delete=models.CASCADE, null=True, blank=True )
    tags = models.ManyToManyField(TagModel, related_name="productmodel_tags")
    description = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='images', default="", null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    manufacturing_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    # Function to return unique slug
    def unique_slug(self):
        unique_slugg = slugify(self.name)
        num = 1
        while ProductModel.objects.filter(slug=unique_slugg).exists():
            unique_slugg = "{}-{}".format(unique_slugg, num)
            num += 1
            break
        return unique_slugg

    # Slugify Function
    def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = self.unique_slug()
      return super().save(*args, **kwargs)

    # Function to return name on table
    def __str__(self):
        return self.name


class StockModel(BaseModel, AddressModel):
    """
    Stock Model to create stock table
    """
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, default=None, related_name='stockmodel_author', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile_number = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='images', default="", null=True, blank=True)
    slug = models.SlugField(unique=True)

    # Function to return unique slug
    def unique_slug(self):
        unique_slugg = slugify(self.author)
        num = 1
        while StockModel.objects.filter(slug=unique_slugg).exists():
            unique_slugg = "{}-{}".format(unique_slugg, num)
            num += 1
            break
        return unique_slugg

    # Slugify Function
    def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = self.unique_slug()
      return super().save(*args, **kwargs)

    # Function to return author name on table
    def __str__(self):
        return self.author.username


class CartModel(BaseModel):
    """
    Cart Model to create cart table
    """
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProductModel, related_name='cartmodel_product', on_delete=models.CASCADE, null=True, blank=True)
    stock = models.ForeignKey(StockModel, related_name='cartmodel_stock', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    # Function to return unique slug
    def unique_slug(self):
        unique_slugg = slugify(self.quantity)
        num = 1
        while CartModel.objects.filter(slug=unique_slugg).exists():
            unique_slugg = "{}-{}".format(unique_slugg, num)
            num += 1
            break
        return unique_slugg

    # Slugify Function
    def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = self.unique_slug()
      return super().save(*args, **kwargs)

    # Function to return product.name + quantity
    def __str__(self):
        return self.product.name + "_" + str(self.quantity)


class CartItem(BaseModel, AddressModel):
    """
    Cart Item Model
    """
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProductModel, related_name='cartitemmodel_product', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)


class AddCartModel(BaseModel, AddressModel):
    """
    Add Cart Model to add items in cart
    """
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    product = models.ManyToManyField(CartItem, related_name='addcartmodel_product', null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    # Function to return unique slug
    def unique_slug(self):
        unique_slugg = slugify(self.product)
        num = 1
        while CartModel.objects.filter(slug=unique_slugg).exists():
            unique_slugg = "{}-{}".format(unique_slugg, num)
            num += 1
            break
        return unique_slugg

    # Slugify Function
    def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = self.unique_slug()
      return super().save(*args, **kwargs)

    # Function to return quantity on table
    def __str__(self):
        return str(self.quantity)


class OrderModel(BaseModel, AddressModel):
    """
    Order Model to create order table
    """
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    ordered_by = models.ForeignKey(User, default=None, related_name='ordermodel_ordered_by', on_delete=models.CASCADE)
    cart = models.ForeignKey(CartModel, related_name='ordermodel_cart', on_delete=models.CASCADE, null=True, blank=True)
    addcart = models.ForeignKey(AddCartModel,  related_name='ordermodel_addcart', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile_number = models.IntegerField(null=True, blank=True)
    total_amount = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    # Function to return unique slug
    def unique_slug(self):
        unique_slugg = slugify(self.ordered_by)
        num = 1
        while OrderModel.objects.filter(slug=unique_slugg).exists():
            unique_slugg = "{}-{}".format(unique_slugg, num)
            num += 1
            break
        return unique_slugg

    # Slugify Function
    def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = self.unique_slug()
      return super().save(*args, **kwargs)

    # Function to return quantity + ordered_by on table
    def __str__(self):
        return str(self.quantity) +"_"+ self.ordered_by.username


class UserAddressModel(models.Model):
    """
    User address model to create address table
    """
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True)

    # Function to return unique slug
    def unique_slug(self):
        unique_slugg = slugify(self.street)
        num = 1
        while UserAddressModel.objects.filter(slug=unique_slugg).exists():
            unique_slugg = "{}-{}".format(unique_slugg, num)
            num += 1
            break
        return unique_slugg

    # Slugify Function
    def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = self.unique_slug()
      return super().save(*args, **kwargs)

    # Function to return street on table
    def __str__(self):
        return self.street


class Payment(models.Model):
    """
    Payment Model to create Payment table to check payment status
    """
    STATUS_CHOICES = (
        ('0', 'Yes'),
        ('1', 'No')
    )
    order = models.ForeignKey(OrderModel, default=None, related_name='ordermodel_order', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices = STATUS_CHOICES, null=True, blank=True)

    # Function to return ordered_by + status on table
    def __str__(self):
        return self.order.ordered_by.username + self.status
