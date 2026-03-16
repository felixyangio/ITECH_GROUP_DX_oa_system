from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Inform, InformRead
from .serializers import InformSerializer, PublishInformSerializer


class InformView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        size = 10
        queryset = Inform.objects.select_related('author').prefetch_related('departments', 'read_records').all()
        total = queryset.count()
        start = (page - 1) * size
        items = queryset[start:start + size]
        serializer = InformSerializer(items, many=True, context={'request': request})
        return Response({'total': total, 'page': page, 'items': serializer.data})

    def post(self, request):
        serializer = PublishInformSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        inform = Inform.objects.create(
            title=data['title'],
            content=data['content'],
            is_top=data.get('is_top', False),
            author=request.user,
        )
        dept_ids = [d for d in data.get('department_ids', []) if d != 0]
        if dept_ids:
            from staff.models import Department
            depts = Department.objects.filter(id__in=dept_ids)
            inform.departments.set(depts)
        return Response(InformSerializer(inform, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)


class InformDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            inform = Inform.objects.get(pk=pk)
        except Inform.DoesNotExist:
            return Response({'detail': 'Announcement not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(InformSerializer(inform, context={'request': request}).data)

    def delete(self, request, pk):
        try:
            inform = Inform.objects.get(pk=pk, author=request.user)
        except Inform.DoesNotExist:
            return Response({'detail': 'Announcement not found or forbidden'}, status=status.HTTP_404_NOT_FOUND)
        inform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InformReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        inform_pk = request.data.get('inform_pk')
        try:
            inform = Inform.objects.get(pk=inform_pk)
        except Inform.DoesNotExist:
            return Response({'detail': 'Announcement not found'}, status=status.HTTP_404_NOT_FOUND)
        InformRead.objects.get_or_create(inform=inform, reader=request.user)
        return Response({'detail': 'Marked as read'})
