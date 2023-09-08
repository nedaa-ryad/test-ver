from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import (LoginForm, MyPasswordChangeForm, MyPasswordResetForm,
                    MySetPasswordForm)

app_name = 'product'

urlpatterns = [
        path('', views.home, name='homePage'),
        path('modern_Collection/', views.modernCollection, name='modern_Collection'),
        path('contemporary_Collection/', views.contemporaryCollection,
            name='contemporary_Collection'),
        path('classic_Collection/', views.classicCollection, name='classic_Collection'),
        path('news/', views.news, name='news'),
        path('about_Us/', views.aboutUs, name='about_Us'),
        path('history/', views.history, name='history'),
        path('contact_Us/', views.contactUs, name='contact_Us'),
        path('category/<slug:val>', views.CategoryView.as_view(), name='category'),
        path('product_detail/<int:id>',
            views.productDetail, name='product_detail'),
        path('All_Products/', views.all_products, name='All_Products'),
        path('profile/', views.ProfileView.as_view(), name='profile'),
        path('address/', views.address, name='address'),
        path('update_address/<int:pk>',
                views.UpdateAddress.as_view(), name='update_address'),
        path('address/<int:pk>/delete/', views.DeleteAddress.as_view(), name='delete_address'),

        path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
        path('cart/', views.show_cart, name='show_cart'),
        path('minus_cart/', views.minus_cart),
        path('plus_cart/', views.plus_cart),
        path('remove_cart/', views.remove_cart),
        
        path('checkout/', views.Checkout.as_view(), name='checkout'),

        path('wishlist/', views.show_wishlist, name='wishlist'),
        path('add_to_wishlist/', views.plus_wishlist),
        path('remove_from_wishlist/', views.minus_wishlist),

        path('search/', views.search, name='search'),

        # authentication
        path('registration/', views.CustomerRegistrationView.as_view(),
                name='customerregistration'),
        path('accounts/login/', auth_views.LoginView.as_view(
        template_name='app/login.html', authentication_form=LoginForm), name='login'),
        path('logout/', auth_views.LogoutView.as_view(next_page='products:login'), name='logout'),
        path('password_change/', auth_views.PasswordChangeView.as_view(
                template_name='app/password_change.html', form_class=MyPasswordChangeForm, success_url='/password_change_done'), name='password_change'),
        path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
                template_name='app/password_change_done.html'), name='password_change_done'),
        
        path("password_reset/", auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', html_email_template_name='app/password_reset_email.html', form_class=MyPasswordResetForm), name="password_reset"),
        path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),
        name="password_reset_done",
        ),
        path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm),
        name="password_reset_confirm",
        ),
        path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
        name="password_reset_complete",
        ),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Nedaa_Ryad Administration'
admin.site.site_title = 'Nedaa_Ryad Administration'
admin.site.site_index_title = 'Welcome To White_Dove Store'