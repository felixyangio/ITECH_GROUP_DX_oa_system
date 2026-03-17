from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import User
from .models import AbsentType, Absent
from .serializers import (
    AbsentTypeSerializer, ResponderSerializer,
    AbsentSerializer, ApplyAbsentSerializer, HandleAbsentSerializer
)


class AbsentTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        types = AbsentType.objects.all()
        return Response(AbsentTypeSerializer(types, many=True).data)


class ResponderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return the first superuser as the default approver
        user = User.objects.filter(is_superuser=True).exclude(pk=request.user.pk).first()
        if not user:
            # Fallback: any is_staff user
            user = User.objects.filter(is_staff=True).exclude(pk=request.user.pk).first()
        if user:
            return Response({'id': user.id, 'email': user.email, 'realname': user.realname})
        return Response({'id': None, 'email': '', 'realname': ''})


class AbsentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        who = request.query_params.get('who', 'my')
        page = int(request.query_params.get('page', 1))
        size = 10
        if who == 'my':
            queryset = Absent.objects.filter(applicant=request.user)
        elif request.user.is_superuser:
            queryset = Absent.objects.all()
        else:
            queryset = Absent.objects.filter(responder=request.user)
        count = queryset.count()
        start = (page - 1) * size
        items = queryset[start:start + size]
        return Response({'count': count, 'results': AbsentSerializer(items, many=True).data})

    def post(self, request):
        serializer = ApplyAbsentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        absent = Absent.objects.create(
            title=data.get('title', ''),
            applicant=request.user,
            absent_type=data['absent_type'],
            responder=data.get('responder'),
            start_date=data['start_date'],
            end_date=data['end_date'],
            request_content=data.get('request_content', ''),
        )
        return Response(AbsentSerializer(absent).data, status=status.HTTP_201_CREATED)


class AbsentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, absent_id):
        if request.user.is_superuser:
            try:
                absent = Absent.objects.get(pk=absent_id)
            except Absent.DoesNotExist:
                return Response({'detail': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                absent = Absent.objects.get(pk=absent_id, responder=request.user)
            except Absent.DoesNotExist:
                return Response({'detail': 'Application not found or forbidden'}, status=status.HTTP_404_NOT_FOUND)
        if absent.status != Absent.STATUS_PENDING:
            return Response({'detail': 'This application has already been processed'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = HandleAbsentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        absent.status = serializer.validated_data['status']
        absent.response_content = serializer.validated_data.get('response_content', '')
        absent.save()
        return Response(AbsentSerializer(absent).data)
