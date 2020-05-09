from django.conf.urls import url
from user_management import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url('create_user/', views.create_user, name='create_user'),
    url('authenticate/', obtain_auth_token, name='authenticate'),
    url('upload_file/', views.upload_file, name='upload_file'),
    url('delete_file/', views.delete_file, name='delete_file'),
    url('fetch_files/', views.get_files, name='fetch_files')
]
