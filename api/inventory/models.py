from django.db import models

# Create your models here.
class Product(models.Model):
    """
    商品
    """
    #論理名 = models.フィールドの型(max_length=最大長, verbose_name=論理名)
    name = models.CharField(max_length=100, verbose_name='商品名')
    price = models.IntegerField(verbose_name='価格')
    description = models.TextField(verbose_name='商品説明', null=True, blank=True)

    class Meta: #追加の設定を記載可能(テーブルコメントやデフォルトのソート順も指定可能)
        db_table = 'product' #テーブルの物理名
        verbose_name = '商品' #テーブルの論理名

class Perchase(models.Model):
    """
    仕入れ
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    purchase_data = models.DateTimeField(verbose_name='仕入日時')

    class Meta:
        db_table = 'purchase'
        verbose_name = '仕入'
    
class Sales(models.Model):
    """
    売上
    """
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    sales_date = models.DateTimeField(verbose_name='売上日時')

    class Meta:
        db_table = 'sales'
        verbose_name = '売上'