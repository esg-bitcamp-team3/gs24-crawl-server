from rest_framework.response import Response
from rest_framework.views import APIView

import requests
import ssl
from apps.market_price.serializers.carbon_price import CarbonPriceSerializer
from config import settings

MARKET_PRICE_API_SERVICE_KEY = settings.MARKET_PRICE_API_SERVICE_KEY

class CarbonPriceView(APIView):
    def get(self, request):
        url = "http://apis.data.go.kr/1160100/service/GetGeneralProductInfoService/getCertifiedEmissionReductionPriceInfo"

        params = {
            "serviceKey": MARKET_PRICE_API_SERVICE_KEY,
            "resultType": "json",
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

            serializer = CarbonPriceSerializer(items, many=True)
            return Response(serializer.data)

        return Response({"error": "Failed to fetch data from API"}, status=500)