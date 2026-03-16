from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from absent.models import Absent
from inform.models import Inform, InformRead
from staff.models import Department


class DepartmentStaffCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = (
            Department.objects
            .annotate(staff_count=Count('staffs'))
            .values('name', 'staff_count')
        )
        return Response(list(data))


class LatestInformView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        informs = Inform.objects.select_related('author').order_by('-create_time')[:10]
        result = []
        for inform in informs:
            reads = InformRead.objects.filter(inform=inform, reader=request.user)
            result.append({
                'id': inform.id,
                'title': inform.title,
                'author': {
                    'realname': inform.author.realname,
                },
                'create_time': inform.create_time,
                'reads': list(reads.values('id')),
            })
        return Response(result)


class LatestAbsentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        absents = (
            Absent.objects
            .select_related('applicant__staff_profile__department')
            .order_by('-create_time')[:10]
        )
        result = []
        for absent in absents:
            applicant = absent.applicant
            try:
                dept_name = applicant.staff_profile.department.name if applicant.staff_profile.department else ''
            except Exception:
                dept_name = ''
            result.append({
                'id': absent.id,
                'requester': {
                    'realname': applicant.realname,
                    'department': {'name': dept_name},
                },
                'start_date': absent.start_date,
                'end_date': absent.end_date,
                'create_time': absent.create_time,
            })
        return Response(result)
