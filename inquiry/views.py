import hashlib
import os
import uuid
from datetime import datetime
from urllib.parse import unquote, urlencode

import jwt
import requests
from django.core.paginator import Paginator
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from inquiry.serializers import DepositWithdrawalResponseSerializer


# Create your views here.

@api_view(['GET'])
def deposit_inquiry_all_money(request: Request):
    access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
    secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
    server_url = "https://api.upbit.com/v1"  # 도메인
    page = request.GET.get('page', '1')  # 페이지
    search_category = request.GET.get('category', 'all')  # 검색어
    search_code = request.GET.get('code', 'KRW')  # 화폐 코드

    print("입출금 종류 :", search_category, ", 페이지 :", page, ", 코드 :", search_code)

    params = {
        'state': 'ACCEPTED',
        # 'currency': search_code if search_code else 'KRW',
        'currency': 'KRW',
    }

    if search_category == "all":
        print("입출금 시")
        res = requests.get(server_url+"/deposits", params=params, headers=create_headers(params, access_key, secret_key)).json()
        params['state'] = 'DONE'
        res += requests.get(server_url+"/withdraws", params=params, headers=create_headers(params, access_key, secret_key)).json()
    else:
        if search_category == "deposit":
            print("입금 시")
            params['state'] = 'ACCEPTED'
            service_url = "/deposits"
        elif search_category == "withdraw":
            print("출금 시")
            params['state'] = 'DONE'
            service_url = "/withdraws"
        else:
            raise ValueError("알 수 없는 코드입니다.")

        res = requests.get(server_url+service_url, params=params, headers=create_headers(params, access_key, secret_key)).json()

    validate_res = DepositWithdrawalResponseSerializer(data=res, many=True)

    if not validate_res.is_valid():
        print("검증 실패")
        return Response(validate_res.errors, status=status.HTTP_400_BAD_REQUEST)

    filtered_list = []
    total_inquiry_assets = 0

    for obj in validate_res.validated_data:
        # print("입금액 :", int(obj['amount']), "입금 날짜 :", obj['done_at'])
        obj['amount'] = int(obj['amount'])
        if obj['state'] == 'ACCEPTED':
            obj['state'] = "입금 성공"
            total_inquiry_assets += int(obj['amount'])
        else:
            obj['state'] = "출금 성공"
            total_inquiry_assets -= int(obj['amount'])
        filtered_list.append(obj)

    sorted_filtered_list = sorted(filtered_list, key=lambda x: x['done_at'], reverse=True)

    paged_list = Paginator(sorted_filtered_list, 20).get_page(page)

    print("총 입금액 :", total_inquiry_assets)

    context = {
        'total_inquiry_assets': total_inquiry_assets,
        'result': paged_list,
        'page': page
    }

    return render(request, 'inquiry/deposit_amount_list.html', context)


def create_headers(params: dict, access_key, secret_key):
    query_string = unquote(urlencode(params, doseq=True)).encode('UTF-8')

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
        'Authorization': authorization,
    }

    return headers

