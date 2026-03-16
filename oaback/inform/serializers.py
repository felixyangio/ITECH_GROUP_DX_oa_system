from rest_framework import serializers
from .models import Inform, InformRead


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    realname = serializers.CharField()
    department = serializers.SerializerMethodField()

    def get_department(self, user):
        try:
            dept = user.staff_profile.department
            if dept:
                return {'name': dept.name}
        except Exception:
            pass
        return {'name': ''}


class DeptSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class InformSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    reads = serializers.SerializerMethodField()
    public = serializers.SerializerMethodField()
    departments = DeptSerializer(many=True, read_only=True)
    read_count = serializers.SerializerMethodField()

    class Meta:
        model = Inform
        fields = ['id', 'title', 'content', 'author', 'create_time',
                  'is_top', 'reads', 'public', 'departments', 'read_count']
        read_only_fields = ['author', 'create_time']

    def get_reads(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if obj.read_records.filter(reader=request.user).exists():
                return [1]
        return []

    def get_public(self, obj):
        return not obj.departments.exists()

    def get_read_count(self, obj):
        return obj.read_records.count()


class PublishInformSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    is_top = serializers.BooleanField(default=False)
    department_ids = serializers.ListField(child=serializers.IntegerField(), required=True)
