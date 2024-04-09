from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, tc, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
      )
      user.is_admin = True
      user.is_superuser = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser,PermissionsMixin):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  last_login = models.DateTimeField(blank=True, null=True)
  groups = models.ManyToManyField(Group, blank=True, related_name='user_groups')


  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name','tc']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin
  

class Saler(models.Model):
    name = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    hotel= models.CharField(max_length=100, null=True)
    addresh = models.CharField(max_length=200, null=True)
    contact = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.name.name} - {self.hotel}"

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    CATERGORY = (
        ('Apartment','Apartment'),
        ('Room', 'Room'),
        ('House', 'House'),
    )

    name=models.CharField(max_length=200, null=True)
    price= models.FloatField(null=True)
    category= models.CharField(max_length=200, null=True, choices=CATERGORY)
    description= models.TextField(max_length=500, null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Payment verified', 'Payment verified'),
    )
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    status= models.CharField(max_length=200, null=True, choices=STATUS)

    
    def __str__(self):
      return f"{self.customer.name} - {self.product}"
    