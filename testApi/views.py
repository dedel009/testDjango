from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from testApi.serializers import GetPrescriptionWorkoutPlanManagementListRequestSerializer


# Create your views here.

def get_prescription_workout_plan_management_list(request: Request):
    """
    # 운동플랜 목록 조회 API

    """
    # 위처럼 """""" 안에 적으면 swagger로 api를 볼 때 설명문이 추가됨.

    request_validator = GetPrescriptionWorkoutPlanManagementListRequestSerializer(data=request.data)
    if not request_validator.is_valid():
        print("양식에 맞지 않습니다.")
        return Response(request_validator.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data: dict = request_validator.validated_data

    center_id = validated_data.get('center_id')
    user_id = validated_data.get('user_id')
    edit_permission = validated_data.get('edit_permission_filter')

