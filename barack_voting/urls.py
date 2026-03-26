from django.contrib import admin
from django.urls import path,include
from elections import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # admin access
    path('',views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('elections/', views.election_list, name='election_list'),
    path('vote/<int:election_id>/', views.vote_election, name='vote_election'),
    # Result viewing
    path('results/<int:election_id>/', views.results_view, name='results'),
    path('not-started/<int:election_id>/', views.not_started, name='not_started'),
    path('already-voted/<int:election_id>/', views.already_voted, name='already_voted'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
