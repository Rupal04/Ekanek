from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class FileSystem(models.Model):
    class Meta(object):
        db_table = 'file_system'

    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=100, blank=True,null=True)
    file_size_in_gb = models.FloatField(blank=False, null=False, default=0)
    s3_file_url = models.URLField(max_length=500)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    compressed_s3_file_url = models.URLField(max_length=500, null=True, blank=True)
    tiny_url = models.URLField(max_length=200, null=True, blank=True)
