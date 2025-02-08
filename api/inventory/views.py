from django.conf import settings
from django.db.models import  F, Value, Sum
from django.db.models.functions import Coalesce, TruncMonth
import pandas
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .exception import BusinessException
from .models import Product, Purchase, Sales, SalesFile, Status
from .serializers import InventorySerializer, ProductSerializer, PurchaseSerializer, SalesSerializer, FileSerializer
        # serializerはDjango内で、Json形式とオブジェクトの形式を変換するためのもの
        # 例1
        #   GETメソッド
        #   serializer = ProductSerializer(オブジェクト形式のデータ)
        #   Response(serializer.data, status.HTTP_200_OK)
        #   ↑ ここで画面に返される値はJson形式となる。
        #
        # 例2
        #   POSTメソッド
        #   serializer = ProductSerializer(Json形式のデータ)
        #   serializer.save()
        #   ↑ ここで渡される値はオブジェクト型になる。
from rest_framework import status

# CSRF設定
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
        print(request.data)
        serializer = ProductSerializer(data=request.data, many=True)
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
    """
    製品モデル(ModelViewSetでの実装バージョン)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class PurchaseView(APIView):
    """
    仕入れモデル
    """
    def get_object(self, pk):
        try:
            return Purchase.objects.get(pk=pk)
        except Purchase.DoesNotExist:
            raise NotFound

    def get(self, request, id=None, format=None):
        if id is None :
            queryset = Purchase.objects.all()
            serializer = PurchaseSerializer(queryset, many=True)
        else:
            product = self.get_object(id)
            serializer = PurchaseSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        仕入れ情報を登録する
        """
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)



class SalesView(APIView):
    """
    売上モデル
    """
    def get_object(self, pk):
        try:
            return Sales.objects.get(pk=pk)
        except Sales.DoesNotExist:
            raise NotFound

    def get(self, request, id=None, format=None):
        if id is None :
            queryset = Sales.objects.all()
            serializer = SalesSerializer(queryset, many=True)
        else:
            product = self.get_object(id)
            serializer = SalesSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        売り上げ情報を登録する
        """
        serializer = SalesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #在庫が売る分の数量を超えないかチェック
        # 在庫テーブルのレコードを取得
        purchase = Purchase.objects.filter(product_id=request.data['product']).aggregate(quantity_sum=Coalesce(Sum('quantity'),0))
        # 卸しテーブルのレコードを取得
        sales = Sales.objects.filter(product_id=request.data['product']).aggregate(quantity_sum=Coalesce(Sum('quantity'),0))
        # 在庫が売る分の数量を超えている場合はエラーレスポンスを返す
        if purchase['quantity_sum'] < (sales['quantity_sum']  + int(request.data['quantity'])):
            raise BusinessException('在庫数量を超過することはできません')
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)



class InventoryView(APIView):
    """
    仕入れ・売り上げ情報を取得する
    """
    def get(self, request, id=None, format=None):
        serializer = InventorySerializer()
        if id is None:
            # idを必ず指定する
            return Response(request.data, status.HTTP_400_BAD_REQUEST)
        else:
            # UNIONするために、それぞれフィールド名を再定義する
            purchase = Purchase.objects.filter(product_id=id).prefetch_related('product').values("id", "quantity", type=Value('1'), date=F('purchase_date'), unit=F('product__price'))
            # Value : 定数値をクエリ内に埋め込む際に使用
            #    例 type=Value('1') 
            #    クエリ結果にtypeというキーを追加し、すべてのレコードで値が1となるように指定する
            # F : モデルフィールドを参照するために使用される。クエリ中でフィールド同士の比較や操作が可能になる。
            #    例 Pruchase.objects.annotate(total_cost=F('quantity')*F('product__price'))
            #    quantityとproduct__priceを掛け合わせた結果をtotal_costというフィールドで取得する。
            #    例 date = F('purchase_date')
            #    purchase_dateフィールドの値をdateとして取得する。
            sales = Sales.objects.filter(product_id=id).prefetch_related('product').values("id", "quantity", type=Value('2'), date=F('sales_date'), unit=F('product__price'))
            queryset = purchase.union(sales).order_by(F("date"))
            serializer = InventorySerializer(queryset, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
    
#@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    ユーザーのログイン処理
    @Args:
      APIView (class) : rest_framework.viewsのAPIViewを受け取る
    """
    # 認証クラスの指定
    authentication_classes = [JWTAuthentication]
    # アクセス許可の指定
    permission_classes = []

    def post(self, request):
        # request.data['access'] = request.META.get('HTTP_AUTHORIZATION')
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        if access:
            response = Response(status=status.HTTP_200_OK)
            max_age = settings.COOKIE_TIME
            response.set_cookie('access', access, httponly=True, max_age=max_age)
            response.set_cookie('refresh', refresh, httponly=True, max_age=max_age)
            return response
        return Response({'errMsg' : 'ユーザーの認証に失敗しました。'}, stauts=status.HTTP_401_UNAUTHORIZED)
    
class RetryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def post(self, request):
        request.data['refresh'] = request.META.get('HTTP_REFRESH_TOKEN')
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        if access:
            response = Response(status=status.HTTP_200_OK)
            max_age = settings.COOKIE_TIME
            response.set_cookie('access', access, httponly=True, max_age=max_age)
            response.set_cookie('refresh', refresh, httponly=True, max_age=max_age)
            return response
        return Response({'errMsg' : 'ユーザーの認証に失敗しました。'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, *args):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
    
# 同期・非同期通信調査
class SalesSyncView(APIView):
    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filename = serializer.validated_data['file'].name

        with open(filename, 'wb') as f:
            f.write(serializer.validated_data['file'].read())

        sales_file = SalesFile(file_name=filename, status=Status.SYNC)
        sales_file.save()

        df= pandas.read_csv(filename)
        for _, row in df.iterrows():
            sales = Sales(
                product_id=row['product'],
                sales_date=row['sales_date'],
                quantity=row['quantity'],
                import_file=sales_file
            )
            sales.save()
        return Response(status=201)

class SalesAsyncView(APIView):
    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filename = serializer.validated_data['file'].name

        with open(filename, 'wb') as f:
            f.write(serializer.validated_data['file'].read())

        sales_file = SalesFile(file_name=filename, status=Status.ASYNC_UNPROCESSED)
        sales_file.save()
        # 売上ファイルからデータを1行ずつ読み取ってDBに保存する以下の処理は非同期で行うこととする。
        """
        df= pandas.read_csv(filename)
        for _, row in df.iterrows():
            sales = Sales(
                product_id=row['product'],
                sales_date=row['sales_date'],
                quantity=row['quantity'],
                import_file=sales_file
            )
            sales.save()
        """
   
        return Response(status=201)

class SalesList(ListAPIView):
    # GenericViewのListAPIViewを使用
    # querysetとserializer_classを定義すれば、いい感じに出力してくれる。
    # 恐らく、return Response(serializer_class(queryset))
    # で返却されている。

    # TruncMonth('sales_date')で年月毎にデータを集計
    # SQLに直すと以下の通り。
    # SELECT CAST(DATE_FORMAT(`sales`.`sales_date`, '%Y-%m-01 00:00:00) AS DATETIME)
    #        SUM(`sales`.`quantity`) AS `monthly_price`
    # FROM   `sales`
    # GROUP BY CAST(DATE_FORMAT(`sales`.`sales_date`, '%Y-%m-01 00:00:00') AS DATETIME)
    # ORDER BY `monthly_date` ASC;
    serializer_class = SalesSerializer
    queryset = Sales.objects.annotate(monthly_date=TruncMonth('sales_date')).values('monthly_date').annotate(monthly_price=Sum('quantity')).order_by('monthly_date')
