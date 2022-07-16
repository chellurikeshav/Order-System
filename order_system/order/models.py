from django import db
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models

# Create your models here.
class Customers(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    count = models.IntegerField()

class Orders(models.Model):
    order_id = models.IntegerField(primary_key=True)
    customer_id = models.ForeignKey(Customers,db_column="customer_id",null=True,on_delete=models.SET_NULL)

class Tables(models.Model):
    occupied = "occupied"
    unoccupied = "unoccupied"
    table_choice = (
        (occupied,"occupied"),
        (unoccupied,"unoccupied")
    )
    table_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customers,db_column="customer_id",null=True,on_delete=models.SET_NULL)
    order_id = models.ForeignKey(Orders,db_column="order_id",null=True,on_delete=models.SET_NULL)
    capacity = models.IntegerField(default=4)
    status = models.CharField(max_length=30,default=unoccupied,choices=table_choice)

class Category(models.Model):
    category_id = models.CharField(max_length=10,primary_key=True)
    category_name = models.CharField(max_length=30)

class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category,db_column="category_id",on_delete=models.CASCADE)
    item_name = models.CharField(max_length=30)
    price = models.IntegerField()

class OrderItems(models.Model):
    order_items_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders,db_column="order_id",on_delete=models.CASCADE)
    menu_id = models.ForeignKey(Menu,db_column="menu_id",on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

class Billing(models.Model):
    billing_id = models.IntegerField(primary_key=True)
    order_id = models.ForeignKey(Orders,db_column="order_id",on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customers,db_column="customer_id",null=True,on_delete=models.SET_NULL)
    total_cost = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)

class Payments(models.Model):
    cash = "cash"
    upi = "upi"
    debit_card = "debit_card"
    credit_card = "credit_card"
    cheque = "cheque"
    payment_choices = (
        (cash,"cash"),
        (upi,"upi"),
        (debit_card,"debit_card"),
        (credit_card,"credit_card"),
        (cheque,"cheque")
    )
    success = "success"
    pending = "pending"
    failed = "failed"
    status_choices = (
        (success,"success"),
        (pending,"pending"),
        (failed,"failed")
    )
    payment_id = models.IntegerField(primary_key=True)
    billing_id = models.ForeignKey(Billing,db_column="billing_id",null=True,on_delete=models.SET_NULL)
    payment_mode = models.CharField(max_length=30,default=cash,choices=payment_choices)
    status = models.CharField(max_length=30,default=success,choices=status_choices)
    date_time = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders,db_column="order_id",on_delete=models.CASCADE)
    ratings = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.CharField(max_length=100,null=True)

class Inventory(models.Model):
    menu_id = models.OneToOneField(Menu,db_column="menu_id",primary_key=True,on_delete=models.CASCADE)
    remaining_quantity = models.IntegerField(default=0)




