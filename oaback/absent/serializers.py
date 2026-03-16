from rest_framework import serializers
from .models import AbsentType, Absent
from authapp.models import User


class AbsentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentType
        fields = ['id', 'name']


class ResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'realname', 'email']


class AbsentSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.realname', read_only=True)
    responder_name = serializers.CharField(source='responder.realname', read_only=True)
    absent_type_name = serializers.CharField(source='absent_type.name', read_only=True)
    absent_type_obj = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Absent
        fields = [
            'id', 'title', 'applicant', 'applicant_name', 'responder', 'responder_name',
            'absent_type', 'absent_type_obj', 'absent_type_name', 'start_date', 'end_date',
            'request_content', 'status', 'status_display', 'response_content', 'create_time'
        ]
        read_only_fields = ['applicant', 'status', 'response_content', 'create_time']

    def get_absent_type_obj(self, obj):
        if obj.absent_type:
            return {'id': obj.absent_type.id, 'name': obj.absent_type.name}
        return None


class ApplyAbsentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    absent_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AbsentType.objects.all(), source='absent_type'
    )
    responder_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='responder', required=False, allow_null=True, default=None
    )
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    request_content = serializers.CharField(required=False, allow_blank=True, default='')


class HandleAbsentSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[Absent.STATUS_APPROVED, Absent.STATUS_REJECTED])
    response_content = serializers.CharField(required=False, allow_blank=True, default='')
