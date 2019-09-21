from django.db import models

"""
csv_cols = [
    'ExhibitionID',
    'ExhibitionNumber',
    'ExhibitionTitle',
    'ConstituentURL', 
    'FirstName',
    'MiddleName',
    'LastName',
    'Suffix',
    'ExhibitionURL',
    'ExhibitionRole',
    'DisplayName',
]
"""

class Exhibition(models.Model):
    moma_id = models.IntegerField()
    moma_number = models.CharField(max_length=50)
    moma_url = models.URLField()
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Artist(models.Model):
    display_name = models.CharField(max_length=200, null=True)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True)
    moma_url = models.URLField()
    suffix = models.CharField(max_length=25, null=True)
    token = models.CharField(max_length=200)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()