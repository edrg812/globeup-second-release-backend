from django.db import models



class SiteSetting(models.Model):
    site_name = models.CharField(max_length=255)
    white_logo = models.ImageField(upload_to='logos/white/')
    dark_logo = models.ImageField(upload_to='logos/dark/')
    favicon = models.ImageField(upload_to='favicons/')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.site_name
