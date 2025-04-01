# cloud_steward_proposals/urls.py

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

urlpatterns = [
    # 1) Admin route (must come first to avoid overshadow by catch-all)
    path('admin/', admin.site.urls),

    # 2) Include your proposals app routes (the REST/DRF endpoints)
    path('api/', include('proposals.urls')),

    # 3) Catch-all for React (serves index.html for any other path)
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
