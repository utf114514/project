from django.db import models


# Create your models here.
class Content(models.Model):
    title = models.CharField('文章名字', max_length=11)
    picture = models.FileField(upload_to='picture')

    def __str__(self):
        return '%s %s' % (self.title, self.picture)
