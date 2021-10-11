from django.db import models


class Base(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    update_date = models.DateTimeField(auto_now=True, editable=False)

    def when_created(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M:%S')

    def when_updated(self):
        return self.update_date.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        abstract = True
