from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import apis

admin.site.site_header = 'PriceNotifier Admin Panel'
admin.site.index_title = 'Database management'
admin.site.site_title = 'PriceNotifier Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('settings', views.settings, name='setting'),

    # Stocks
    path('new_stock', views.add_stock, name='new_stock'),
    path('modify_stock/<uuid:id>', views.modify_stock, name='modify_stock'),

    # Other prices
    path('new_other', views.add_other, name='new_other'),
    path('modify_other/<uuid:id>', views.modify_other, name='modify_other'),

    # API routes
    path('api/stock/<str:code>/current', apis.get_current_price),
    path('api/stock/<str:code>/years/<int:years>', apis.get_year_price),
]

handler404 = 'app.views.handle404'
