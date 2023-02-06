from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from .models import ProductModel, TagModel, CategoryModel, OrderModel, CartModel, StockModel, UserAddressModel, AddCartModel, CartItem, Payment
from .forms import ProductForm, OrderForm, CartOrderForm
from datetime import date
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import JsonResponse


def Home(request):
    return HttpResponse("World!!!!!!")


class ProductCreate(CreateView):
    """
    Class based view to create Product
    """
    form_class = ProductForm
    template_name = "ProductApp/productmodel_form.html"
    success_url = reverse_lazy('ProductApp:productlist')

    def form_valid(self, form):
        tag_data = self.request.POST['tagname']
        tagging  = tag_data.split(',')
        category = self.request.POST['categoryname']
        data = form.save(commit=False)

        x = CategoryModel.objects.filter(title=category)
        if x :
            data.category = x[0]
        else:
            v = CategoryModel.objects.create(title=category)
            data.category = v
        data.save()

        for tag in tagging:
            try:
                var = TagModel.objects.get(name=tag)
                data.tags.add(var)
            except:
                data.tags.create(name=tag)

        return redirect('ProductApp:productlist')


class ProductUpdate(UpdateView):
    """
    Class based view to update Product
    """
    model = ProductModel
    form_class = ProductForm
    success_url = reverse_lazy('ProductApp:list')
    template_name = 'ProductApp/productmodel_update.html'

    def form_valid(self, form):
        tag_data = self.request.POST['tagname']
        tagging  = tag_data.split(' ')
        data = form.save()
        category = self.request.POST['categoryname']
        x = CategoryModel.objects.filter(title=category)
        if x :
            data.category = x[0]
        else:
            v = CategoryModel.objects.create(title=category)
            data.category = v
        
        data.save()

        for tag in tagging:
            try:
                var = ProductModel.objects.get(name=tag)
                taggers = data.tags.all()
                if var in tagging:
                    continue
                else:
                    data.tags.add(var)
            except:
                data.tags.create(name=tag)

        return redirect('ProductApp:detail', data.id)


class ProductDetail(DetailView):
    """
    Class based view for detail of Product
    """
    model = ProductModel
    template_name = "ProductApp/productmodel_detail.html"

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        prod_id = self.kwargs['pk']
        prod = get_object_or_404(ProductModel, id=self.kwargs['pk'])
        cart = CartModel.objects.get(product=prod)
        cart.save()
        lst=[]
        a = CartItem.objects.all()
        for i in a:
            lst.append(i.product.name)
        context["quantity"] = cart.quantity
        context["cart_items"] = lst
        return context


# function to delete a product by authorized users only
def remove(request, pk):
    product = ProductModel.objects.get(id=pk)
    if product.blogger == request.user or request.user.is_staff:
        return redirect('ProductApp:productdelete', pk=product.id)
    else:
        return HttpResponse("not authorized!!!!")
    return redirect('ProductApp:productdetail', pk=product.id)


# function to edit a product by authorized users only
def edit(request, pk):
    product=ProductModel.objects.get(id=pk)
    if product.blogger == request.user or request.user.is_staff:
        return redirect('ProductApp:productupdate',pk=product.id)
    else:
        return HttpResponse("not authorized to update!!!!")
    return redirect('ProductApp:productdetail', pk=product.id)


class ProductList(ListView):
    """
    Class based view to list out Products
    """
    model = ProductModel

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        tshirts = ProductModel.objects.filter(category__title='T-Shirts')
        shirt = ProductModel.objects.filter(category__title='Shirt')
        jacket = ProductModel.objects.filter(category__title='Jacket')
        jeans = ProductModel.objects.filter(category__title='Jeans')
        context['tshirts'] = tshirts
        context['shirt'] = shirt
        context['jacket'] = jacket
        context['jeans'] = jeans
        return context


class ProductDelete(DeleteView):
    """
    Class based view to delete Product
    """
    model = ProductModel
    template_name = 'ProductApp/productmodel_confirm.html'
    success_url = reverse_lazy('ProductApp:productlist')


def order(self, request):
    return redirect('ProductApp:productlist')


class OrderCreate(CreateView):
    """
    Class based view to create a order for a product
    """
    form_class = OrderForm
    template_name = 'productapp/ordermodel_form.html'
    success_url = reverse_lazy('ProductApp:order_done')

    def form_valid(self,form):
        order = form.save()
        pk = self.kwargs['pk']
        product = ProductModel.objects.get(id=pk)
        order.cart = CartModel.objects.get(product=product)
        order.save()
        cart = CartModel.objects.get(product=product)
        cart.quantity = cart.quantity - order.quantity
        cart.save()
        address= self.request.POST['add1']
        location = UserAddressModel.objects.get(street=address)
        order.street = location.street
        order.city = location.city
        order.state = location.state
        order.country = location.country
        order.pin_code = location.pin_code
        order.latitude = location.latitude
        order.longitude = location.longitude
        order.save()
        return redirect('ProductApp:payment', pk=product.id)

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        prod_id = self.kwargs['pk']
        prod = get_object_or_404(ProductModel, id=self.kwargs['pk'])
        p = prod.name
        cart = CartModel.objects.get(product=prod)
        cart.save()
        address = UserAddressModel.objects.all()
        context["prod"] = p
        context["quantity"] = cart.quantity
        context["address"] = address
        return context


# function to return the page after order is done
def order_done(request):
    return render(request, 'productapp/order_done.html')


class OrderList(ListView):
    """
    Class based view to list out all the orders
    """
    model = OrderModel

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        p = Payment.objects.all()
        lst = []
        for i in p:
            lst.append(i.order)
        context['p'] = p
        context['lst'] = lst
        return context


class OrderDetail(DetailView):
    """
    Class based view for details of a order
    """
    model = OrderModel

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        cartlist = AddCartModel.objects.all()
        context['cartlist'] = cartlist
        return context


class CartList(ListView):
    """
    Class based view to list out the cart items
    """
    model = AddCartModel

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = AddCartModel.objects.all()
        amount = 0
        for item in cart:
            for i in item.product.all():
                amount = amount + ( i.product.price * i.quantity)
        items = CartItem.objects.all().count()
        context['amount'] = amount
        context['items'] = items
        return context


# function to add item in cart
def addcart(request, pk):
    product = ProductModel.objects.get(id=pk)
    cart = AddCartModel.objects.get(id=31)
    b = CartItem.objects.create(product=product)
    b.save()
    products=[]
    a = CartItem.objects.all()
    for q in a:
        products.append(q.product)
    for p in products:
        try:
            var = CartItem.objects.get(product=p)
            cart.product.add(var)
        except:
            cart.product.create(product=p)
    cart.save()
    c = CartItem.objects.get(product=product)
    c.quantity = 1
    c.save()
    return redirect('ProductApp:productdetail', pk=product.id)


# function to remove item from cart
def removecart(request, pk):
    product = ProductModel.objects.get(id=pk)
    item = CartItem.objects.get(product=product)
    item.delete()
    return redirect('ProductApp:cartlist')


class AddCartUpdate(UpdateView):
    """
    Class based view to update cart
    """
    model = CartItem
    fields = ['quantity']
    template_name = 'ProductApp/addcartmodel_update.html'

    def form_valid(self, form):
        form.save()
        return redirect('ProductApp:cartlist')


class OrderCart(CreateView):
    """
    Class based view to create a order for a cart
    """
    form_class = CartOrderForm
    template_name = 'productapp/cartordermodel_form.html'
    success_url = reverse_lazy('ProductApp:order_done')

    def form_valid(self,form):
        order = form.save()
        pk = self.kwargs['pk']
        cart = AddCartModel.objects.get(id = 31)
        order.addcart = cart
        address= self.request.POST['add11']
        location = UserAddressModel.objects.get(street=address)
        order.street = location.street
        order.city = location.city
        order.state = location.state
        order.country = location.country
        order.pin_code = location.pin_code
        order.latitude = location.latitude
        order.longitude = location.longitude
        order.save()
        return redirect('ProductApp:paymentcart', pk=order.id)

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        address = UserAddressModel.objects.all()
        cart = AddCartModel.objects.all()
        amount = 0
        lst=[]
        for item in cart:
            for i in item.product.all():
                amount = amount + ( i.product.price * i.quantity)
                lst.append(i.product)
        context['lst'] = lst
        context['amount'] = amount
        context["address"] = address
        return context


# function for payment of order for a product
def PaymentOrder(request, pk):
    amount = 0
    order = OrderModel.objects.get(id=pk)
    quantity = order.quantity
    amount = amount + (order.cart.product.price * quantity)
    context = {'amount':amount , 'product':order.cart.product.name, 'order':order}
    return render(request, 'productapp/payment.html', context=context)


# function for payment of order for a cart
def PaymentCart(request, pk):
    cart = AddCartModel.objects.all()
    order = OrderModel.objects.get(id=pk)
    amount = 0
    lst=[]
    for item in cart:
        for i in item.product.all():
            amount = amount + ( i.product.price * i.quantity)
            lst.append(i.product)
    context= {'amount':amount, 'order':order}
    return render(request, 'productapp/payment.html', context=context)


# function to create payment model and change payment status
def PaymentStatus(request, pk):
    order = OrderModel.objects.get(id=pk)
    if Payment.objects.filter(order=order).first() is not None:
        p = Payment.objects.filter(order=order).first()
        p.status = 0
        p.save()
    else:
        p = Payment.objects.create(order=order)
        p.status = 0
        p.save()
    return JsonResponse(data=1, safe=False)
