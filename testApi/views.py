import hashlib
import os
import uuid
from urllib.parse import unquote, urlencode

import jwt
import requests

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from testApi.serializers import DepositResponseSerializer


# Create your views here.

@api_view(['GET'])
def inquiry_all_money(request: Request):
    access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
    secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
    server_url = "https://api.upbit.com"  # 도메인

    params = {
        'state': 'ACCEPTED'
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

    response = res.json()

    validate_res = DepositResponseSerializer(data=response, many=True)

    if validate_res.is_valid():
        print("검증 성공")
        return Response(validate_res.data, status=status.HTTP_200_OK)
    else:
        print("response 검증 실패")
        return Response(validate_res.errors, status=status.HTTP_400_BAD_REQUEST)


