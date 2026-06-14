from rest_framework import serializers
from datetime import datetime
from .models import Order, Worker, Workshop, Company

class DateQuerySerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(required=False)
    month = serializers.IntegerField(required=False)
    def validate(self, data):
        now = datetime.now()
        data["year"] = data.get("year", now.year)
        data["month"] = data.get("month", now.month)
        return data

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

class CompanyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class WorkshopViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'

class WorkerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'


