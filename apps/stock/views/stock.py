import json
import time
from collections import Counter
import redis
import requests
from konlpy.tag import Okt
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.stock.serializers.stock import ResponseBodySerializer
from config import settings

INVEST_APP_KEY = settings.INVEST_APP_KEY
INVEST_SECRET_KEY = settings.INVEST_SECRET_KEY

TOKEN_REDIS_KEY = "koreainvestment_access_token"

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_access_token():
    token_data = redis_client.get(TOKEN_REDIS_KEY)
    if token_data:
        token_info = json.loads(token_data)
        expires_at = token_info.get("expires_at", 0)
        now = time.time()
        if expires_at - now > 300:
            return token_info["access_token"]

    url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
    }
    payload = {
        "grant_type": "client_credentials",
        "appkey": INVEST_APP_KEY,
        "appsecret": INVEST_SECRET_KEY,
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        expires_in = data.get("expires_in", 86400)

        if access_token:
            now = time.time()
            token_info = {
                "access_token": access_token,
                "expires_at": now + expires_in
            }
            redis_client.set(TOKEN_REDIS_KEY, json.dumps(token_info), ex=expires_in)
            return access_token
        else:
            raise Exception("access_token이 응답에 없습니다.")
    else:
        print(response)
        raise Exception(f"토큰 요청 실패: {response.status_code} {response.text}")

class StockView(APIView):

    def get(self, request):
        code = request.GET.get("code")
        access_token = get_access_token()

        url = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/search-info"

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {access_token}",
            "appkey": INVEST_APP_KEY,
            "appsecret": INVEST_SECRET_KEY,
            "tr_id": "FHKST01010100",
            "custtype": "P"
        }

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": code
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()

            serializer = ResponseBodySerializer(data)
            return Response(serializer.data)
        else:

            return Response({"error": "Failed to fetch data from Korea Invest API"}, status=500)
