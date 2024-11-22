from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status

class ProductView(APIView):
    """
    商品操作に関する関数
    """
    def get(self, request, format=None):
        """
        商品の一覧を取得する
        """
        # querysetはデータベースからのオブジェクトのコレクションを表す。
        # 0以上のフィルターを含めて絞り込むことができる。
        # 例1 全件取得 .all(): select * from Product;
        queryset = Product.objects.all() 
        # 例2 額1000円以上 filter(price__gt=1000): select * from Product where price > 1000;
        queryset = Product.objects.filter(price__gt=1000)
        # 例3 金額昇順 order_by('price'): select * from product order by price asc;
        queryset = Product.objects.order_by('price')
        # 例4 項目指定 values('name','price'): select name, price from product;
        queryset = Product.objects.values('name', 'price')
        # その他はDjango公式ドキュメントを参照せよ

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer