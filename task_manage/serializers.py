from rest_framework import serializers
from .models import *
import base64
from django.utils.safestring import mark_safe



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckListOption
        fields = '__all__'




class QCTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = QCTask
        fields = '__all__'
        
        
class QCStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = QCStatus
        fields = '__all__'




class TaskSerializer(serializers.ModelSerializer):
    # description_base64 = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'


    def get_description(self, obj):
        # Use mark_safe to mark the HTML content as safe
        return mark_safe(obj.description)


    # def get_description_base64(self, obj):
    #     # Encode the description field as base64
    #     if obj.description:
    #         description_bytes = obj.description.encode("ascii")
    #         base64_bytes = base64.b64encode(description_bytes)
    #         return base64_bytes.decode("ascii")
    #     return None
        
        
# class TaskDetailSerializer(TaskSerializer):
#     pairs = serializers.SerializerMethodField()

#     class Meta:
#         model = Task
#         fields = TaskSerializer.Meta.fields

#     def get_pairs(self, obj):
#         pairs = []
#         for checklist_option, qc_check in zip(obj.checklist_options.all(), obj.qc_check.all()):
#             pair = {
#                 "checklist_id": checklist_option.id,
#                 "qc_check_id": qc_check.id
#             }
#             pairs.append(pair)
#         return pairs




#
        
        

class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = '__all__'
        

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
     


class TaskActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskActivity
        fields = '__all__' 