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






