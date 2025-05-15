from collections import Counter

from konlpy.tag import Okt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers import ElectraTokenizer, ElectraForSequenceClassification, AutoTokenizer, \
    AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import requests

from config import settings

NAVER_CLIENT_ID = settings.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET

class KoBertSentimentAnalysisView(APIView):
    MODEL_NAME = "monologg/koelectra-base-finetuned-nsmc"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_NAME, num_labels=2)
        self.model.to(self.device)
        self.model.eval()
        self.okt = Okt()

    def get_keywords_from_api(self, query, display, target):
        url = f"https://openapi.naver.com/v1/search/{target}.json?query={query}&display={display}&start=1&sort=sim"
        headers = {
            "X-Naver-Client-Id": NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []

        data = response.json()
        items = data.get("items", [])
        texts = []

        for item in items:
            desc = item.get("description") or item.get("title") or ""
            texts.append(desc)

        return texts


    def extract_keywords(self, texts):
        keywords = []
        for text in texts:
            nouns = self.okt.nouns(text)
            keywords.extend([n for n in nouns if len(n) > 1])
        word_freq = Counter(keywords)
        return [word for word, freq in word_freq.most_common(30)]  # 상위 30개 키워드

    def predict_sentiment(self, texts):
        if not texts:
            return []

        inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=128)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1).cpu().numpy()  # numpy 배열로 변환

        results = []
        for text, prob in zip(texts, probs):
            neg = float(prob[0])
            pos = float(prob[1])
            results.append({
                "text": text,
                "negative_prob": neg,
                "positive_prob": pos,
            })

        return results

    def predict_sentiment_texts(self, texts):
        if not texts:
            return None

        results = []
        for text in texts:

            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)

            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = F.softmax(outputs.logits, dim=1)
                pred = torch.argmax(probs, dim=1).item()

            label = "긍정" if pred == 1 else "부정"
            results.append({"text":text, "label": label})

        return results

    def count_sentiment_texts(self, texts):
        if not texts:
            return None

        negatives = 0
        positives = 0
        for text in texts:

            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)

            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = F.softmax(outputs.logits, dim=1)
                pred = torch.argmax(probs, dim=1).item()

            if pred == 1:
                positives += 1
            else:
                negatives += 1

        return {
            "negatives": negatives,
            "positives": positives,
        }

    def get(self, request):
        query = request.GET.get('query', "")
        display = request.GET.get('display', 10)

        if not query:
            return Response({"error": "query 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        all_texts = []

        for target in ["news", "cafearticle", "blog"]:
            texts = self.get_keywords_from_api(query, display, target)
            all_texts.extend(texts)

        result = self.count_sentiment_texts(all_texts)

        return Response({
            "result": result,
        })
