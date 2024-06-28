from rest_framework import serializers

# 운동 플랜 목록 (플랜 관리) API 관련


class GetPrescriptionWorkoutPlanManagementListRequestSerializer(serializers.Serializer):
    center_id = serializers.IntegerField(
        help_text='센터 ID'
    )

    user_id = serializers.UUIDField(
        help_text='트레이너 UUID'
    )

    edit_permission_filter = serializers.ChoiceField(
        choices=("SHARED", "OWNED", "ALL"),
        help_text="편집 권한으로 필터링"
    )

