from django.db import models

# Create your models here.
class Upload(models.Model):
    file1 = models.FileField(upload_to='excel_files/file1', max_length=500)
    file2 = models.FileField(upload_to='excel_files/file2', max_length=500)

    class Meta:
        db_table = 'Excel Upload'