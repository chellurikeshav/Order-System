from cmath import cos
from configparser import NoOptionError
from math import remainder
from os import uname
from rest_framework import viewsets
from yaml import serialize
from .models import Customers,Orders,Tables,Category,Menu,OrderItems,Billing,Feedback,Inventory,Payments
from .serializers import ( CustomersSerializer,
                            OrdersSerializer,
                            TablesSerializer,
                            CategorySerializer,
                            MenuSerializer,
                            OrderItemsSerializer,
                            BillingSerializer,
                            FeedbackSerializer,
                            InventorySerializer,
                            PaymentsSerializer
)

from rest_framework.response import Response
from rest_framework.decorators import action
import time
import threading

class Queue:
    def __init__(self):
        self.Q = []
    
    def push(self,id):
        self.Q.append(id)

    def pop(self):
        try:
            return self.Q.pop(0)
        except:
            return "Empty"
    
    def top(self):
        try:
            return self.Q[0]
        except:
            return "Empty"

wait_customeres = Queue()

class CustomersViewset(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer

    def create(self, request):
        customer_data = request.data  
        id = (Customers.objects.last())
        if id:
            id = id.customer_id + 1
        else:
            id = int(time.time())
        new_customer = Customers(customer_id = id,count = customer_data.get('count'))
        new_customer.save()
        serializer = CustomersSerializer(Customers.objects.get(customer_id = id))  
        return Response(serializer.data)    

class TablesViewset(viewsets.ModelViewSet):
    queryset = Tables.objects.all()
    serializer_class = TablesSerializer

    def create(self, request):
        table_data = request.data
        new_table = Tables(capacity = table_data.get('capacity'))
        new_table.save()
        id = (Tables.objects.last())
        serializer = TablesSerializer(Tables.objects.get(table_id = id.table_id)) 
        return Response(serializer.data)


    @action(methods=['POST'], detail=False)
    def assign(self,request):
        assign_data = request.data
        count = Customers.objects.filter(customer_id = assign_data.get("customer_id")).first().count
        table = Tables.objects.filter(capacity__gte = count,status = Tables.unoccupied).order_by("capacity").first()
        if table:
            customer_instance = Customers.objects.filter(customer_id = assign_data.get("customer_id")).first()
            table.customer_id = customer_instance
            table.status = Tables.occupied
            table.save()
            return Response({'message':f'Table No.{table.table_id} alloted Successfully'})

        wait_customeres.push(request.data.get("customer_id"))
        return Response({'message':"No table Found! Wait for a while"})
    
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuViewset(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def list(self,request):
        query = Menu.objects.all().order_by("category_id")
        serializer = MenuSerializer(query,many = True)
        return Response(serializer.data)
    
    def create(self, request):
        menu_data = request.data
        category_instance = Category.objects.filter(category_id = menu_data.get('category_id')).first()
        new_menu = Menu(category_id = category_instance, item_name = menu_data.get('item_name'),price = menu_data.get('price'))
        new_menu.save()
        id = (Menu.objects.last())
        serializer = MenuSerializer(Menu.objects.get(menu_id = id.menu_id)) 
        return Response(serializer.data)

class OrdersViewset(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

    def create(self, request):
        order_data = request.data
        id = Orders.objects.last()
        if id:
            id = id.order_id + 1
        else:
            id = int(time.time())
        customer_instance = Customers.objects.filter(customer_id = order_data.get('customer_id')).first()
        new_order = Orders(order_id = id,customer_id = customer_instance)
        new_order.save()

        assign_tables = Tables.objects.filter(customer_id = order_data.get('customer_id'))
        for table in assign_tables:
            table.order_id = new_order
            table.save()

        serializer = OrdersSerializer(Orders.objects.get(order_id = id)) 
        return Response(serializer.data)
    

class OrderItemsViewset(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer

        
    def create(self, request):
        order_items_data = request.data
        order_instance = Orders.objects.filter(order_id = order_items_data.get('order_id')).first()
        unavailable = "unvailable"
        ordered = "ordered"
        message = {ordered:[],unavailable:[]}

        for item,count in order_items_data.get("items").items():

            menu_instance = Menu.objects.filter(menu_id = int(item)).first()
            cuisine = Inventory.objects.get(menu_id = menu_instance)

            if count <= cuisine.remaining_quantity:
                cuisine.remaining_quantity = cuisine.remaining_quantity - count
                cuisine.save()
                
                new_order_item = OrderItems(order_id = order_instance,menu_id = menu_instance,quantity = count)
                new_order_item.save()
                message[ordered].append(f'{count} {menu_instance.item_name} Ordered')
            else:
                message[unavailable].append(f'Only {cuisine} units of {menu_instance.item_name} available.')
        
        return Response(message)
    

class BillingViewset(viewsets.ModelViewSet):    
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

    def create(self, request):
        billing_data = request.data
        id = Billing.objects.last()
        if id:
            id = id.billing_id + 1
        else:
            id = int(time.time())
        cost = 0
        order_instance = Orders.objects.filter(order_id = billing_data.get('order_id')).first()
        customer_instance = Customers.objects.filter(customer_id = order_instance.customer_id.customer_id).first()
        items = OrderItems.objects.filter(order_id = order_instance)
        for item in items:
            menu_instance = Menu.objects.filter(menu_id = item.menu_id.menu_id).first()
            cost += (menu_instance.price)*item.quantity

        new_billing = Billing(billing_id = id, customer_id = customer_instance,order_id = order_instance,total_cost = cost)
        new_billing.save()
        serializer = BillingSerializer(Billing.objects.get(billing_id = id))
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=False)
    def showbill(self,request):
        bill_data = request.data
        bill = {}

        order_instance = Orders.objects.filter(order_id = bill_data.get('order_id')).first()
        bill_instance = Billing.objects.filter(order_id = order_instance).first()

        bill["order_id"] = bill_data.get('order_id')
        bill["customer_id"] = order_instance.customer_id.customer_id
        bill["items"] = []

        items = OrderItems.objects.filter(order_id = order_instance)
        serializer = OrderItemsSerializer(items,many = True).data

        for item in serializer:
            new_item = {}

            item_id = item.get('menu_id')       
            menu_instance = Menu.objects.filter(menu_id = item_id).first()

            new_item["item_name"] = menu_instance.item_name
            new_item["quantity"] = item.get("quantity")
            new_item["value"] = item.get("quantity")*menu_instance.price
            
            bill['items'].append(new_item)
        
        bill["total_value"] = bill_instance.total_cost
        return Response(bill)


    
class PaymentsViewset(viewsets.ModelViewSet):    
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def create(self, request):
        payment_data = request.data
        id = int(time.time())
        billing_instance = Billing.objects.filter(billing_id = payment_data.get('billing_id')).first()
        mode = payment_data.get('payment_mode')
        pay_status = payment_data.get('status')
        if not mode:
            mode = Payments.cash
        if not pay_status:
            pay_status = Payments.success
        new_payment = Payments(payment_id = id,billing_id = billing_instance,payment_mode = mode,status = pay_status)
        new_payment.save()
        serializer = PaymentsSerializer(Payments.objects.get(payment_id = id))

        if pay_status == Payments.success:
            ordered_id = Billing.objects.filter(billing_id = payment_data.get('billing_id')).first().order_id.order_id
            order_instance = Orders.objects.filter(order_id = ordered_id).first()
            tables = Tables.objects.filter(order_id = order_instance)

            for table in tables:
                table.customer_id = None
                table.order_id = None
                table.status = Tables.unoccupied
                table.save()
        return Response(serializer.data)

class FeedbackViewset(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def create(self, request):
        feedback_data = request.data
        order_instance = Orders.objects.filter(order_id = feedback_data.get('order_id')).first()
        rating = feedback_data.get('ratings')
        if not rating:
            rating = 3
        new_feedback = Feedback(order_id = order_instance,ratings = rating,comments = feedback_data.get('comments'))
        new_feedback.save()
        id = (Feedback.objects.last())
        serializer = FeedbackSerializer(Feedback.objects.get(feedback_id = id.feedback_id))
        return Response(serializer.data)

class InventoryViewset(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer  

    def create(self,request):
        inventory_data = request.data

        menu_instance = Menu.objects.filter(menu_id = inventory_data.get('menu_id')).first()
        new_inventory = Inventory(menu_id = menu_instance, remaining_quantity = inventory_data.get('remaining_quantity'))
        new_inventory.save()
        id = (Inventory.objects.last())
        serializer = InventorySerializer(Inventory.objects.get(menu_id = id.menu_id))
        return Response(serializer.data)