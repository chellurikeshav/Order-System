from order.viewsets import  (   CustomersViewset,
                                OrdersViewset,
                                TablesViewset,
                                CategoryViewset,
                                MenuViewset,
                                OrderItemsViewset,
                                BillingViewset,
                                FeedbackViewset,
                                InventoryViewset,
                                PaymentsViewset            
)

from rest_framework import routers

router = routers.DefaultRouter()

router.register('customers',CustomersViewset)
router.register('orders',OrdersViewset)
router.register('tables',TablesViewset)
router.register('category',CategoryViewset)
router.register('menu',MenuViewset)
router.register('orderitems',OrderItemsViewset)
router.register('billing',BillingViewset)
router.register('feedback',FeedbackViewset)
router.register('payments',PaymentsViewset)
router.register('inventory',InventoryViewset)
