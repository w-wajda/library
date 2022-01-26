from base import urls_api
from django.contrib import admin
from django.urls import (
    include,
    path
)
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls_api)),
    path('api-token-auth/', obtain_auth_token),

    path('password_reset', PasswordResetView.as_view()),
    path('password_reset_done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_comfirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



