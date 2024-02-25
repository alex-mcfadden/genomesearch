from django.contrib import admin
from django.urls import include, path  # 👈 Add include here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('genome_finder.urls'))
]
