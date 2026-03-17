from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ResetPwdSerializer(serializers.Serializer):
    oldpwd = serializers.CharField()
    pwd1 = serializers.CharField(min_length=6)
    pwd2 = serializers.CharField(min_length=6)

    def validate(self, data):
        if data['pwd1'] != data['pwd2']:
            raise serializers.ValidationError('Passwords do not match')
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'realname', 'department', 'is_superuser']

    def get_department(self, obj):
        try:
            dept = obj.staff_profile.department
            if dept:
                return {'id': dept.id, 'name': dept.name}
        except Exception:
            pass
        return {'id': None, 'name': ''}
