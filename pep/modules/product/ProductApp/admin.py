from django.contrib import admin
from modules.product.ProductApp.models import ProductModel, CategoryModel, TagModel, OrderModel, StockModel, CartModel, UserAddressModel, AddCartModel, CartItem, Payment

admin.site.register(ProductModel)
admin.site.register(CategoryModel)
admin.site.register(TagModel)
admin.site.register(OrderModel)
admin.site.register(StockModel)
admin.site.register(CartModel)
admin.site.register(UserAddressModel)
admin.site.register(AddCartModel)
admin.site.register(CartItem)
admin.site.register(Payment)
