import hashlib
import os
import uuid
from urllib.parse import unquote, urlencode

import jwt
import requests
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
    server_url = "https://api.upbit.com"  # 도메인

    params = {
        'state': 'ACCEPTED',
        'currency': 'KRW',
    }
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

    res = requests.get(server_url+"/v1/deposits", params=params, headers=headers)

    validate_res = DepositWithdrawalResponseSerializer(data=res.json(), many=True)

    if not validate_res.is_valid():
        print("검증 실패")
        return Response(validate_res.errors, status=status.HTTP_400_BAD_REQUEST)

    filtered_list = []
    total_inquiry_assets = 0

    for obj in validate_res.validated_data:
        print("입금액 :", int(obj['amount']), "입금 날짜 :", obj['done_at'])
        obj['amount'] = int(obj['amount'])
        obj['state'] = "입금 성공"
        total_inquiry_assets += int(obj['amount'])
        filtered_list.append(obj)

    print("총 입금액 :", total_inquiry_assets)

    context = {
        'total_inquiry_assets': total_inquiry_assets,
        'result': filtered_list
    }

    return render(request,'inquiry/deposit_amount_list.html', context)

# @api_view(['GET'])
# def withdrawal_inquiry_all_money(request: Request):
#     access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
#     secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
#     server_url = "https://api.upbit.com"  # 도메인
#
#     params = {
#         'state': 'ACCEPTED',
#         'currency': 'KRW',
#     }
#     query_string = unquote(urlencode(params, doseq=True)).encode('UTF-8')
#
#     m = hashlib.sha512()
#     m.update(query_string)
#     query_hash = m.hexdigest()
#
#     payload = {
#         'access_key': access_key,
#         'nonce': str(uuid.uuid4()),
#         'query_hash': query_hash,
#         'query_hash_alg': 'SHA512',
#     }
#
#     jwt_token = jwt.encode(payload, secret_key)
#     authorization = 'Bearer {}'.format(jwt_token)
#     headers = {
#         'Authorization': authorization,
#     }
#
#     res = requests.get(server_url+"/v1/deposits", params=params, headers=headers)
#
#     validate_res = DepositWithdrawalResponseSerializer(data=res.json(), many=True)
#
#     if not validate_res.is_valid():
#         print("검증 실패")
#         return Response(validate_res.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     filtered_list = []
#     total_inquiry_assets = 0
#
#     for obj in validate_res.validated_data:
#         print("입금액 :", int(obj['amount']), "입금 날짜 :", obj['done_at'])
#         obj['amount'] = int(obj['amount'])
#         obj['state'] = "입금 성공"
#         total_inquiry_assets += int(obj['amount'])
#         filtered_list.append(obj)
#
#     print("총 입금액 :", total_inquiry_assets)
#
#     context = {
#         'total_inquiry_assets': total_inquiry_assets,
#         'result': filtered_list
#     }
#
#     return render(request,'inquiry/deposit_amount_list.html', context)




