from rest_framework import serializers
from .models import Order, Worker, Workshop, Company

class WorkerSerializers(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = Worker
        fields = ['id', 'full_name', 'position', 'phone']
    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name} {obj.dad_name}"

class WorkshopSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    class Meta:
        model = Workshop
        fields = ['address', 'company_name']

class OrderSerializer(serializers.ModelSerializer):
    worker_info = WorkerSerializers(source="worker", read_only=True)
    admin_info = WorkerSerializers(source="admin", read_only=True)
    workshop_info = WorkshopSerializer(source="worker.workshop", read_only=True)
    type_work_display = serializers.CharField(source="get_type_work_display")
    class Meta:
        model = Order
        fields = ['id', 'car_number', 'car_name', 'type_work', 'type_work_display',
            'price', 'arrival_time', 'work_start_time', 'work_end_time',
            'comments', 'finding', 'worker_info', 'admin_info', 'workshop_info']