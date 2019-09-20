from django.db import models

class Exhibition(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Artist(models.Model):
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    token = models.CharField(max_length=200)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()