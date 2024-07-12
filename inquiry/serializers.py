from rest_framework import serializers


class DepositWithdrawalResponseSerializer(serializers.Serializer):
    type = serializers.CharField(
        help_text="입출금 종류"
    )
    uuid = serializers.UUIDField(
        help_text="입금에 대한 고유 아이디"
    )
    currency = serializers.CharField(
        help_text="화폐를 의미하는 영문 대문자 코드"
    )
    net_type = serializers.CharField(
        help_text="입금 네트워크",
        allow_blank=True,
        allow_null=True
    )
    txid = serializers.CharField(
        help_text="입금의 트랜잭션 아이디"
    )
    state = serializers.CharField(
        help_text="입금 상태"
    )
    created_at = serializers.DateTimeField(
        help_text="입금 생성 시간"
    )
    done_at = serializers.DateTimeField(
        help_text="입금 완료 시간"
    )
    amount = serializers.FloatField(
        help_text="입금 수량"
    )
    fee = serializers.FloatField(
        help_text="입금 수수료"
    )
    transaction_type = serializers.CharField(
        help_text="입금 유형"
    )


# 동적 시리얼라이저 개발 소스
# class ClimitDynamicRequestSerializer(serializers.Serializer):
#     user_id = serializers.UUIDField(help_text="유저 UUID")
#     machine_id = serializers.UUIDField(help_text="머신 UUID")
#     assignment_workout_plan_id = serializers.IntegerField(help_text='처방된 운동 플랜 ID', min_value=1)
#     def __init__(self, **kwargs):
#         self.request_data = kwargs.get("data", None)
#         super().__init__(self, **kwargs)
#         print("request_data :::", self.request_data)
#         if self.request_data:
#             self.field_list: list = list(self.request_data.keys())
#             for field in self.field_list:
#                 if field == "user_id":
#                     # 유저 id 필드 생성
#                     self.fields['user_id'] = serializers.UUIDField(help_text="유저 UUID")
#                 elif field == "machine_id":
#                     # 머신 id 필드 생성
#                     self.fields['machine_id'] = serializers.UUIDField(help_text="머신 UUID")
#                 elif field == "assignment_workout_plan_id" or field == "workout_plan_id":
#                     # 처방 운동 플랜 id 필드 생성
#                     # 필드명이 2개일 때 처리
#                     self.fields['assignment_workout_plan_id'] = \
#                         serializers.IntegerField(help_text='처방된 운동 플랜 ID', min_value=1, required=False)
#                     if field == "workout_plan_id":
#                         self.initial_data['assignment_workout_plan_id'] = self.request_data.get("workout_plan_id")
#                 else:
#                     # 해당되는 필드명이 없을 때 error
#                     raise ValueError("필드명을 찾을 수 없습니다.")



