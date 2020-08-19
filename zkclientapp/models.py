from django.db import models

# Create your models here.
class merkletree(models.Model):
    class Meta:
        db_table = 'merkletree'
    mid = models.IntegerField(db_column='MID')
    tree_data = models.TextField(max_length=40000, db_column='tree_data', blank=False)
    blockNumber = models.IntegerField(db_column='blockNumber', default=1)

class contract(models.Model):
	class Meta:
		db_table = 'contract'
	conName = models.CharField(max_length=20, db_column='conName')
	conType = models.CharField(max_length=20, db_column='conType')
	conAddr = models.CharField(max_length=500, db_column='conAddr')
	time = models.CharField(max_length=80, db_column='time')
	owner = models.CharField(max_length=500, db_column='owner')
	totalAmount = models.IntegerField(db_column='totalAmount')
	shortName = models.CharField(max_length=20, db_column='shortName')

class transactions(models.Model):
	class Meta:
		db_table = 'transactions'
	traType = models.CharField(max_length=20, db_column='traType')
	username = models.CharField(max_length=20, db_column='username')
	vin = models.IntegerField(db_column='vin')
	vout = models.IntegerField(db_column='vout')
	input_notes = models.CharField(max_length=20, db_column='input_notes')
	output_specs = models.CharField(max_length=1000, db_column='output_specs')
	time = models.CharField(max_length=80, db_column='time')