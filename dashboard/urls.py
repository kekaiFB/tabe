from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('user.urls')),    
    path('table/', include('table.urls')), 
    path('chaining/', include('smart_selects.urls')),
    path('permission/', include('permission.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
 
from user.views import ErrorHandler

for code in (400, 403, 404, 500):
    vars()['handler{}'.format(code)] = ErrorHandler.as_view(error_code=code)


