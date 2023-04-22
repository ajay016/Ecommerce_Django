from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

# class Customer(models.Model):
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     first_name = models.CharField(max_length=200, null=True)
#     last_name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(max_length=200, null=True)
#     phone = models.CharField(max_length=200, null=True)
    
#     def __str__(self):
#         return self.first_name or ''

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Email is required")
        
        if not password:
            raise ValueError("Password is required")
        
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            phone = phone
        )
        user.set_password(password)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin

        user.save(using=self._db)

        return user
    
    def create_staffuser(self, first_name, last_name, email, phone, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name= last_name,
            
            phone = phone,
            password = password,
            is_staff = True
        )

        return user
    
    def create_superuser(self, first_name, last_name, email, phone, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name= last_name,
            
            phone = phone,
            password = password,
            is_staff = True,
            is_admin = True
        )

        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.email or ''
    
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name or ''
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active
    
    def has_perm(self, perm, obj=None):
        return self.admin
    
    def has_module_perms(self, app_label):
        return True
    
    # def get_by_natural_key(self, email):
    #     return self.get(email=email)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class MainCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name or ''
    
class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.main_category.name + '--' + self.name or ''
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.category.main_category.name + '--' + self.category.name + '--' + self.name or ''

class Product(models.Model):
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    flash_sale  = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    # if a image is missing it will throw an error, to avoid this this function is implmented
    # with @property we can call imageURL as attribute in the templates "product.imageURL"
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        
        return url
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.image.url
    
class Order(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
                
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    
        