from rest_framework import serializers
from .models import Worker, DailyTask, WorkHours, Salary
from .services import get_land_details, get_culture_details, get_equipment_details

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class WorkerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'first_name', 'last_name', 'worker_type', 'status', 'zone']

class DailyTaskSerializer(serializers.ModelSerializer):
    land_name = serializers.SerializerMethodField(read_only=True)
    culture_name = serializers.SerializerMethodField(read_only=True)
    equipment_name = serializers.SerializerMethodField(read_only=True)
    worker_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DailyTask
        fields = '__all__'
        read_only_fields = ['assigned_by']

    def get_land_name(self, obj):
        if not obj.land_id: return None
        land = get_land_details(obj.land_id)
        return land.get('name') if land else f"Land #{obj.land_id}"

    def get_culture_name(self, obj):
        if not obj.culture_id: return None
        culture = get_culture_details(obj.culture_id)
        return culture.get('name') if culture else f"Culture #{obj.culture_id}"

    def get_equipment_name(self, obj):
        if not obj.equipment_id: return None
        equip = get_equipment_details(obj.equipment_id)
        return equip.get('name') if equip else f"Equip #{obj.equipment_id}"
        
    def get_worker_name(self, obj):
        return f"{obj.worker.first_name} {obj.worker.last_name}"

class WorkHoursSerializer(serializers.ModelSerializer):
    worker_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = WorkHours
        fields = '__all__'
        
    def get_worker_name(self, obj):
        return f"{obj.worker.first_name} {obj.worker.last_name}"

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ['total']

class WorkerSummarySerializer(serializers.ModelSerializer):
    # This serializer aggregates different data.
    # Expects a specific context or pre-fetched data from a view.
    recent_hours = serializers.SerializerMethodField(read_only=True)
    latest_salary = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Worker
        fields = ['id', 'first_name', 'last_name', 'worker_type', 'status', 'recent_hours', 'latest_salary']

    def get_recent_hours(self, obj):
        hours = obj.hours.all().order_by('-date')[:5]
        return WorkHoursSerializer(hours, many=True).data

    def get_latest_salary(self, obj):
        salary = obj.salaries.all().order_by('-month').first()
        if salary:
            return SalarySerializer(salary).data
        return None

class MonthlySummarySerializer(serializers.Serializer):
    worker_id = serializers.IntegerField()
    month = serializers.DateField()
    total_regular_hours = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_overtime = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
