from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    # JWTAuthentication内の get_headerメソッドを継承して使う。
    # リクエストヘッダーにトークンを保存して、認証を行う仕組みに変えている。
    # (通常はAuthorizationヘッダーに入れる)

    # このメソッドは、JWTAuthenticationを呼び出す時に、実行される？
    def get_header(self, request):
        # cookie内のaccessという名前からトークンを取得
        token = request.COOKIES.get('access')
        # request.META は、リクエストのHTTPヘッダーなどを保持する
        # 通常、DRFのJWT認証は Authorization ヘッダーにトークンを保持するが、
        # このコードはクッキーから取得したトークンを HTTP_AUTHORIZATION に設定することで、通常のヘッダー形式に変換する。
        request.META['HTTP_AUTHORIZATION'] = '{header_type} {access_token}'.format(
            header_type ='Bearer', access_token=token
        )
        # '{キー1}{キー2}'.format(キー1=バリュー1, キー2=バリュー2)
        # で、出力は、「バリュー1バリュー2」となる。
        # pythonのフォーマット構文という基本の構文
        
        # refreshトークンも同様にしてrequestヘッダーに入れ込む
        refresh = request.COOKIES.get('refresh')
        request.META['HTTP_REFRESH_TOKEN'] = '{header_type}:{refresh_token}'.format(
            header_type='refresh', refresh_token=refresh
        )
        return super().get_header(request)