from django.db import models

# Create your models here.
class merkletree(models.Model):
    class Meta:
        db_table = 'merkletree'
    mid = models.IntegerField(db_column='MID',primary_key=True)
    tree_data = models.TextField(max_length=40000, db_column='tree_data', blank=False)
    blockNumber = models.IntegerField(db_column='blockNumber', default=1)
