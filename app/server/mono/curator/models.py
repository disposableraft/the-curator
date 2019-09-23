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
    moma_id = models.IntegerField(null=True)
    moma_number = models.CharField(max_length=50)
    moma_url = models.URLField(null=True)
    title = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

class Artist(models.Model):
    display_name = models.CharField(max_length=200, null=True, unique=True)
    exhibition = models.ManyToManyField(Exhibition)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    middle_name = models.CharField(max_length=200, null=True)
    moma_url = models.URLField(null=True)
    suffix = models.CharField(max_length=25, null=True)
    token = models.CharField(max_length=200)

    class Meta:
        ordering = ('display_name',)

    def __str__(self):
        return self.display_name