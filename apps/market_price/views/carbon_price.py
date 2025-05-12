from json import dumps

from kafka import KafkaProducer
from rest_framework.response import Response
from rest_framework.views import APIView

import requests
import ssl
from apps.market_price.serializers.carbon_price import CarbonPriceSerializer
from config import settings

MARKET_PRICE_API_SERVICE_KEY = settings.MARKET_PRICE_API_SERVICE_KEY

class CarbonPriceView(APIView):
    def get(self, request):
        basDt = request.query_params.get('basDt')
        beginBasDt = request.query_params.get('beginBasDt')
        isinCd = request.query_params.get('isinCd')
        itmsNm = request.query_params.get('itmsNm')
        likeItmsNm = request.query_params.get('likeItmsNm')

        url = "http://apis.data.go.kr/1160100/service/GetGeneralProductInfoService/getCertifiedEmissionReductionPriceInfo"

        params = {
            "serviceKey": MARKET_PRICE_API_SERVICE_KEY,
            "resultType": "json",
        }

        if basDt:
            params["basDt"] = basDt
        if beginBasDt:
            params["beginBasDt"] = beginBasDt
        if isinCd:
            params["isinCd"] = isinCd
        if itmsNm:
            params["itmsNm"] = itmsNm
        if likeItmsNm:
            params["likeItmsNm"] = likeItmsNm

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

            serializer = CarbonPriceSerializer(items, many=True)

            producer = KafkaProducer(
                acks=0,
                compression_type='gzip',
                bootstrap_servers=['broker의 ip:9092'],
                value_serializer=lambda x: dumps(x).encode('utf-8')
            )

            producer.send('market_price', serializer.data)
            producer.flush()

            return Response(serializer.data)

        return Response({"error": "Failed to fetch data from API"}, status=500)