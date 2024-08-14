"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

handler400 = 'core.config.views.bad_request_400_view'
handler403 = 'core.config.views.http_forbidden_403_view'
handler404 = 'core.config.views.page_not_found_404_view'
handler500 = 'core.config.views.server_error_500_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.apps.singer.urls')),
] + debug_toolbar_urls()
