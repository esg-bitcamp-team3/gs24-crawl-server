import json
import time
from collections import Counter
import redis
import requests
from konlpy.tag import Okt
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.stock.serializers.stock import StockResponseBodySerializer
from apps.stock.views.invest_mixin import InvestmentViewMixin


class StockView(InvestmentViewMixin, APIView):
    def get(self, request):
        code = request.GET.get("code")
        access_token = self.get_access_token()

        url = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/search-info"

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {access_token}",
            "appkey": self.invest_app_key,
            "appsecret": self.invest_secret_key,
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

            serializer = StockResponseBodySerializer(data)
            return Response(serializer.data)
        else:

            return Response({"error": "Failed to fetch data from Korea Invest API"}, status=500)
