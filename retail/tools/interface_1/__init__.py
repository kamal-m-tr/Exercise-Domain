# Retail Domain Tools - Interface 1

# Getter Tools
from .get_user_info import GetUserInfo
from .get_supplier_info import GetSupplierInfo
from .get_product_info import GetProductInfo
from .get_purchase_order_info import GetPurchaseOrderInfo
from .get_purchase_order_items import GetPurchaseOrderItems
from .get_sales_order_info import GetSalesOrderInfo
from .get_sales_order_items import GetSalesOrderItems
from .get_shipping_info import GetShippingInfo

# Setter Tools - Supplier
from .create_supplier import CreateSupplier
from .update_supplier import UpdateSupplier

# Setter Tools - Product
from .create_product import CreateProduct
from .update_product import UpdateProduct

# Setter Tools - User
from .create_user import CreateUser
from .update_user import UpdateUser

# Setter Tools - Purchase Order
from .create_purchase_order import CreatePurchaseOrder
from .update_purchase_order import UpdatePurchaseOrder
from .add_purchase_order_item import AddPurchaseOrderItem

# Setter Tools - Sales Order
from .create_sales_order import CreateSalesOrder
from .update_sales_order import UpdateSalesOrder
from .add_sales_order_item import AddSalesOrderItem

# Setter Tools - Shipping
from .create_shipping import CreateShipping
from .update_shipping import UpdateShipping

# Escalation
from .transfer_to_human import TransferToHuman


ALL_TOOLS_INTERFACE_1 = [
    # Getters (8)
    GetUserInfo,
    GetSupplierInfo,
    GetProductInfo,
    GetPurchaseOrderInfo,
    GetPurchaseOrderItems,
    GetSalesOrderInfo,
    GetSalesOrderItems,
    GetShippingInfo,
    # Setters (15)
    CreateSupplier,
    UpdateSupplier,
    CreateProduct,
    UpdateProduct,
    CreateUser,
    UpdateUser,
    CreatePurchaseOrder,
    UpdatePurchaseOrder,
    AddPurchaseOrderItem,
    CreateSalesOrder,
    UpdateSalesOrder,
    AddSalesOrderItem,
    CreateShipping,
    UpdateShipping,
    TransferToHuman,
]
