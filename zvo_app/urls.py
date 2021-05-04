from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    path('', views.home),
    path('about', views.about),
    path('demos', views.demos),
    path('news', views.news),
    path('bookings', views.bookings),
    path('user/send', views.bookings),
    path('login', views.login),
    path('admin/login', views.login),
    path('admin', views.admin),
    path('admin/inbox-sort/<str:sortBy>', views.admin_sort),
    path('admin/view/message/<int:msgId>', views.admin_view),
    path('admin/delete/message/<int:msgId>', views.admin_delete_message),
    path('admin/post/article', views.news),
    path('admin/delete/article/<int:articleId>', views.admin_delete_article),
    path('admin/post/demo', views.demos),
    path('admin/delete/demo/<int:demoId>', views.admin_delete_demo),
    path('admin/update/about', views.about),
    path('admin/update/video', views.home),
    path('admin/update', views.admin),
    path('admin/logout', views.admin_logout),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

