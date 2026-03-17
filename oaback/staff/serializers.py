from rest_framework import serializers
from .models import Department, Staff
from authapp.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'intro']


class StaffSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    realname = serializers.CharField(source='user.realname', read_only=True)
    department = serializers.SerializerMethodField()
    date_joined = serializers.DateField(source='join_date', read_only=True)

    class Meta:
        model = Staff
        fields = ['id', 'email', 'realname', 'department', 'status', 'uid', 'date_joined']

    def get_department(self, obj):
        if obj.department:
            return {'id': obj.department.id, 'name': obj.department.name}
        return None


class AddStaffSerializer(serializers.Serializer):
    realname = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department',
        required=False, allow_null=True, default=None
    )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already registered')
        return value
