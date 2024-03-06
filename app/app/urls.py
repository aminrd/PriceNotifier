from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

admin.site.site_header = 'PriceNotifier Admin Panel'
admin.site.index_title = 'Database management'
admin.site.site_title = 'PriceNotifier Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('settings', views.settings, name='setting'),
]

handler404 = 'app.views.handle404'
