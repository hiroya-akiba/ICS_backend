from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer, PurchaseSerializer, SalesSerializer
from rest_framework import status

class ProductView(APIView):
    """
    商品操作に関する関数
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound

    def get(self, request, id=None, format=None):
        """
        商品の一覧を取得する
        """
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
        """
        if id is None :
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
        else:
            product = self.get_object(id)
            serializer = ProductSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data) # POST内容と対応するシリアライザーを呼び出す
        # Validationが通らなかった場合に例外を投げる (Falseの時はスルーして.save()が実行されてしまう)
        serializer.is_valid(raise_exception=True)
        # 検証したデータを永続化する
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def put(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, id, format=None):
        product = self.get_object(id)
        product.delete()
        return Response(status= status.HTTP_200_OK)
    
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PurchaseView(APIView):
    def post(self, request, format=None):
        """
        仕入れ情報を登録する
        """
        serializer = PurchaseSerializer(Data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class SalesView(APIView):
    def post(self, request, format=None):
        """
        仕入れ情報を登録する
        """
        serializer = SalesSerializer(Data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
