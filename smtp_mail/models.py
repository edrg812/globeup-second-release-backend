from django.db import models


class SMTPMail(models.Model):
    MAILER_CHOICES = [
        ('smtp', 'SMTP'),
        ('sendmail', 'Sendmail'),
        ('mailgun', 'Mailgun'),
        ('ses', 'Amazon SES'),
        ('postmark', 'Postmark'),
        ('sparkpost', 'SparkPost'),
    ]

    mailer = models.CharField(max_length=50, choices=MAILER_CHOICES)
    host = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    encryption = models.CharField(max_length=50, choices=[('ssl', 'SSL'), ('tls', 'TLS'), ('none', 'None')], default='none')
    from_address = models.EmailField()
    from_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.mailer} - {self.from_address}"
