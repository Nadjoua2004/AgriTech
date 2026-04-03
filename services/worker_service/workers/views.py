from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render

def index_view(request):
    return render(request, 'index.html')
from decimal import Decimal
import datetime

from .models import Worker, DailyTask, WorkHours, Salary
from .serializers import (
    WorkerSerializer, WorkerListSerializer, DailyTaskSerializer,
    WorkHoursSerializer, SalarySerializer, WorkerSummarySerializer,
    MonthlySummarySerializer
)
from .events import publish_task_completed, publish_salary_calculated, publish_worker_created
from .permissions import decode_jwt_from_request

# ================= WORKERS =================

class WorkerViewSet(viewsets.ModelViewSet):
    """
    Workers CRUD
    GET    /api/workers/                    → list all workers (manager/supervisor only)
    POST   /api/workers/                    → create worker (manager/supervisor)
    GET    /api/workers/<id>/               → worker detail
    PUT    /api/workers/<id>/               → update worker (manager/supervisor)
    DELETE /api/workers/<id>/               → deactivate worker (manager/supervisor)
    GET    /api/workers/<id>/summary/       → worker + their hours + latest salary
    """
    queryset = Worker.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkerListSerializer
        return WorkerSerializer

    def get_queryset(self):
        user_data = getattr(self.request, 'user_data', None)
        if not user_data:
            return Worker.objects.none()
            
        role = user_data.get('role')
        user_id = user_data.get('user_id')

        # Workers can only see themselves
        if role in ['field_worker', 'irrigation_worker', 'equipment_operator']:
            return Worker.objects.filter(user_id=user_id)
            
        return super().get_queryset()

    def perform_create(self, serializer):
        worker = serializer.save()
        publish_worker_created(worker.id, worker.worker_type, worker.zone)

    def perform_destroy(self, instance):
        # Soft delete instead of real deletion
        instance.status = 'inactive'
        instance.save()

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        worker = self.get_object()
        # Allows sending ?month=2024-04 to filter hours within summary
        month_str = request.query_params.get('month')
        if month_str:
            try:
                date_filter = datetime.datetime.strptime(month_str, '%Y-%m').date()
                hours = worker.hours.filter(date__year=date_filter.year, date__month=date_filter.month)
                
                total_hours = sum(h.hours_worked for h in hours)
                total_overtime = sum(h.overtime for h in hours)
                
                salary = worker.salaries.filter(month=date_filter).first()
                
                return Response({
                    "worker_id": worker.id,
                    "month": month_str,
                    "total_regular_hours": total_hours,
                    "total_overtime": total_overtime,
                    "total_salary": salary.total if salary else None,
                })
            except ValueError:
                return Response({"error": "Invalid month format. Use YYYY-MM"}, status=400)
                
        serializer = WorkerSummarySerializer(worker)
        return Response(serializer.data)


# ================= TASKS =================

class DailyTaskViewSet(viewsets.ModelViewSet):
    """
    Daily Tasks CRUD
    GET    /api/tasks/?date=2024-04-01&status=pending
    POST   /api/tasks/
    PATCH  /api/tasks/<id>/status/
    """
    serializer_class = DailyTaskSerializer

    def get_queryset(self):
        user_data = getattr(self.request, 'user_data', None)
        if not user_data:
            return DailyTask.objects.none()
            
        role = user_data.get('role')
        user_id = user_data.get('user_id')
        queryset = DailyTask.objects.all()

        if role in ['field_worker', 'irrigation_worker', 'equipment_operator']:
            # Workers only see their own tasks
            queryset = queryset.filter(worker__user_id=user_id)

        date_filter = self.request.query_params.get('date')
        status_filter = self.request.query_params.get('status')
        if date_filter:
            queryset = queryset.filter(date=date_filter)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def perform_create(self, serializer):
        user_data = getattr(self.request, 'user_data', None)
        assigned_by = user_data.get('user_id') if user_data else 0
        serializer.save(assigned_by=assigned_by)

    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(DailyTask.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        task.status = new_status
        task.save()
        
        # Publish event when marked as done
        if new_status == 'done':
            publish_task_completed(task.worker_id, task.land_id, task.culture_id, task.date)
            
        return Response(DailyTaskSerializer(task).data)


# ================= WORK HOURS =================

class WorkHoursViewSet(viewsets.ModelViewSet):
    serializer_class = WorkHoursSerializer

    def get_queryset(self):
        queryset = WorkHours.objects.all()
        user_data = getattr(self.request, 'user_data', None)
        if not user_data:
            return queryset.none()
            
        role = user_data.get('role')
        user_id = user_data.get('user_id')

        if role in ['field_worker', 'irrigation_worker', 'equipment_operator']:
            queryset = queryset.filter(worker__user_id=user_id)
            
        month_filter = self.request.query_params.get('month')
        if month_filter:
            try:
                dt = datetime.datetime.strptime(month_filter, '%Y-%m')
                queryset = queryset.filter(date__year=dt.year, date__month=dt.month)
            except ValueError:
                pass
                
        return queryset

    @action(detail=False, methods=['get'])
    def summary(self, request):
        worker_id = request.query_params.get('worker')
        month_str = request.query_params.get('month')
        
        if not worker_id or not month_str:
            return Response({"error": "Please provide worker and month (YYYY-MM)"}, status=400)
            
        try:
            dt = datetime.datetime.strptime(month_str, '%Y-%m')
            worker = get_object_or_404(Worker, id=worker_id)
            hours = worker.hours.filter(date__year=dt.year, date__month=dt.month)
            return Response({
                "worker_id": worker.id,
                "month": month_str,
                "total_regular_hours": sum(h.hours_worked for h in hours),
                "total_overtime": sum(h.overtime for h in hours)
            })
        except ValueError:
             return Response({"error": "Invalid month format"}, status=400)


# ================= SALARY =================

class SalaryViewSet(viewsets.ModelViewSet):
    serializer_class = SalarySerializer
    queryset = Salary.objects.all()

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        worker_id = request.data.get('worker_id')
        month_str = request.data.get('month')
        
        if not worker_id or not month_str:
            return Response({"error": "worker_id and month are required"}, status=400)

        # 1. Validation
        worker = get_object_or_404(Worker, id=worker_id)
        try:
            dt = datetime.datetime.strptime(month_str, '%Y-%m')
            first_day_of_month = datetime.date(dt.year, dt.month, 1)
        except ValueError:
            return Response({"error": "Invalid month format. Use YYYY-MM"}, status=400)

        # 2. Sum hours
        hours = worker.hours.filter(date__year=dt.year, date__month=dt.month)
        
        total_overtime_hours = sum(h.overtime for h in hours)
        
        # 3. Base salary logic (fetching from last month or defaulting)
        last_salary = worker.salaries.filter(month__lt=first_day_of_month).order_by('-month').first()
        base_salary = last_salary.base_salary if last_salary else Decimal('1000.00')

        # 2. Calculate Overtime (e.g., base_salary / 160h = hourly rate * 1.5)
        hourly_rate = base_salary / Decimal(160)
        overtime_pay = Decimal(total_overtime_hours) * hourly_rate * Decimal('1.5')

        # 4. Create or Update Salary
        salary, created = Salary.objects.update_or_create(
            worker=worker,
            month=first_day_of_month,
            defaults={
                'base_salary': base_salary,
                'overtime_pay': round(overtime_pay, 2)
            }
        )

        # 5. Publish to RabbitMQ
        publish_salary_calculated(worker.id, first_day_of_month, float(salary.total))

        return Response(SalarySerializer(salary).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# ================= MOCK VIEWS =================

from .mock_data import MOCK_LANDS, MOCK_CULTURES, MOCK_EQUIPMENTS

@api_view(['GET'])
def mock_lands(request):
    return Response(list(MOCK_LANDS.values()))

@api_view(['GET'])
def mock_land_detail(request, pk):
    return Response(MOCK_LANDS.get(int(pk), {}))

@api_view(['GET'])
def mock_cultures(request):
    return Response(list(MOCK_CULTURES.values()))

@api_view(['GET'])
def mock_equipments(request):
    return Response(list(MOCK_EQUIPMENTS.values()))

@api_view(['GET'])
def mock_auth_me(request):
    return Response({"user_id": 1, "role": "farm_manager", "name": "Mock Auth User"})
