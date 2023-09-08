from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import (PasswordResetTokenGenerator,
                                        default_token_generator)
from django.contrib.auth.views import redirect_to_login
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, resolve_url
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import CustomerProfileForm, CustomerRegistrationForm
from .models import Cart, Customer, Product, Wishlist

UserModel = get_user_model()
User = get_user_model()

def home(request):
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/home.html', locals())

def modernCollection(request):
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/modern.html', locals())

def contemporaryCollection(request):
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/contemporary.html', locals())

def classicCollection(request):
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/classic.html', locals())

def news(request):
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/news.html', locals())

def aboutUs(request):
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/about-us.html', locals())

def history(request):
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/history.html', locals())

def contactUs(request):
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/contact_us.html', locals())

def signIn(request):
    return render(request, 'app/sign_in.html')

class CategoryView(View):
    def get(self, request, val):
        product_list = Product.objects.filter(category=val) 
        totalaitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalaitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/product_list.html', locals())

def all_products(request):
    all_product = Product.objects.all()
    paginator = Paginator(all_product, 12)
    page_number = request.GET.get("page")
    all_product = paginator.get_page(page_number)
    
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    
    context = {
        'all_product': all_product,
        'totalaitem': totalaitem, 
        'wishlist': wishlist,
    }

    return render(request, 'app/all_products.html', context)

@login_required
def productDetail(request, id):
    products = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=products.category).exclude(id=id)[:4]
    wishlist_products = Wishlist.objects.filter(Q(product=products) & Q(user=request.user))

    totalaitem = 0
    wishlist = 0
    totalaitem = len(Cart.objects.filter(user=request.user))
    wishlist = len(Wishlist.objects.filter(user=request.user))

    context = {
        'products': products,
        'related_products': related_products,
        'totalaitem': totalaitem,
        'wishlist': wishlist,
    }
    return render(request, 'app/product_detail.html', context)

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Welcome, Your Registration Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'app/customerregistration.html', locals())

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalaitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalaitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            zipCode = form.cleaned_data['zipCode']
            
            reg = Customer(user=user,name=name, locality=locality,city=city,mobile=mobile,zipCode=zipCode)
            reg.save()
            messages.success(request, 'Profile Save Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'app/profile.html', locals()) 

def address(request):
    add = Customer.objects.filter(user=request.user)
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())

class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalaitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalaitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/update_address.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.zipCode = form.cleaned_data['zipCode']
            add.save()
            messages.success(request, 'Profile Save Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return redirect('products:address')

class DeleteAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)

        totalaitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalaitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))

        context = {
            'add': add,
            'totalaitem': totalaitem,
            'wishlist': wishlist,
        }

        return render(request, 'app/delete_address.html', context)

    def post(self, request, pk):
        add = Customer.objects.get(pk=pk)
        add.delete()
        messages.success(request, 'Address deleted successfully')
        return redirect('products:address')

class PasswordContextMixin:
    extra_context = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context

def send_password_reset_email(request, email, token):
    current_site = get_current_site(request)
    subject = 'Password reset on {}'.format(current_site.domain)
    message = render_to_string('app/password_reset_email.html', {
        'request': request,
        'email': email,
        'user': request.user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
        'token': token,
        'protocol': 'http',
    })
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

class PasswordResetView(FormView):
    template_name = 'app/password_reset.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']

        if not User.objects.filter(email=email).exists():
            messages.error(self.request, 'This email address is not associated with any account.')
            return redirect('products:password_reset')

        token = PasswordResetTokenGenerator().make_token(form.get_user())
        send_password_reset_email(self.request, email, token)
        
        messages.success(self.request, 'An email with password reset instructions has been sent.')

        return super().form_valid(form)

INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"

class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = "app/password_reset_done.html"
    title = _("Password reset sent")

class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = "set-password"
    success_url = reverse_lazy("/password_reset_complete")
    template_name = "app/password_reset_confirm.html"
    title = _("Enter new password")
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context["validlink"] = True
        else:
            context.update(
                {
                    "form": None,
                    "title": _("Password reset unsuccessful"),
                    "validlink": False,
                }
            )
        return context

class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = "app/password_reset_complete.html"
    title = _("Password reset complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context

@login_required
def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())

    user = request.user
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    messages.success(request, "Product added to cart.")
    return redirect('products:show_cart')

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        if p.product.discountPrice is not None:
            value = p.quantity * p.product.discountPrice
        else:
            value = p.quantity * p.product.price
        amount += value
    totalamount = amount + 30
    totalaitem = 0
    wishlist = 0
    totalaitem = len(Cart.objects.filter(user=request.user))
    wishlist = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', locals())

def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart_item = Cart.objects.filter(
            Q(product=product_id) & Q(user=request.user)).first()
        if cart_item is not None:
            cart_item.quantity += 1
            cart_item.save()
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                if p.product.discountPrice is not None:
                    value = p.quantity * p.product.discountPrice
                else:
                    value = p.quantity * p.product.price
                amount += value
            totalamount = amount + 30
            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart_item = Cart.objects.filter(
            Q(product=product_id) & Q(user=request.user)).first()
        if cart_item is not None:
            cart_item.quantity -= 1
            cart_item.save()
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                if p.product.discountPrice is not None:
                    value = p.quantity * p.product.discountPrice
                else:
                    value = p.quantity * p.product.price
                amount += value
            totalamount = amount + 30
            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart_items = Cart.objects.filter(Q(product=product_id) & Q(user=request.user))
        
        cart_items.delete()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            if p.product.discountPrice is not None:
                value = p.quantity * p.product.discountPrice
            else:
                value = p.quantity * p.product.price
            amount += value
        totalamount = amount + 30
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

class Checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0
        for p in cart_items:
            if p.product.discountPrice is not None:
                value = p.quantity * p.product.discountPrice
            else:
                value = p.quantity * p.product.price
            amount += value
        totalamount = amount + 30
    
        totalaitem = 0
        wishlist = 0
        if request.user.is_authenticated:
            totalaitem = len(Cart.objects.filter(user=request.user))
            wishlist = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/checkout.html', locals())

@login_required
def show_wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    totalaitem = 0
    wishlist = 0
    totalaitem = len(Cart.objects.filter(user=request.user))
    wishlist = len(Wishlist.objects.filter(user=request.user))
    
    context = {
        'wishlist_items': wishlist_items,
        'totalaitem': totalaitem,
        'wishlist': wishlist,
    }
    return render(request, 'app/wishlist.html', context)

def plus_wishlist(request):
    if request.method == 'GET':
        user = request.user
        product_id = request.GET['product_id']
        product = Product.objects.get(id=product_id)
        Wishlist(user=user, product=product).save()
        data = {
            'success': True,
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        product = Product.objects.get(id=product_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'success': True,
            'message': 'Wishlist Removed Successfully',
        }
        return JsonResponse(data)

def search(request):
    query = request.GET['search']
    totalaitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalaitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains= query))
    return render(request, 'app/search.html', locals())