from rest_framework import serializers
from .models import *
import base64
import binascii




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
    # decoded_description = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'


    


#     def get_description_base64(self, obj):
#         # Encode the description field as base64
#         if obj.description:
#             description_bytes = obj.description.encode("utf-8")
#             base64_bytes = base64.b64encode(description_bytes)
#             return base64_bytes.decode("utf-8")
#         return None
        
        
        
#     def get_decoded_description(self, obj):
#         # Decode the base64-encoded description back to its original form
#         if obj.description:
#             try:
#                 base64_bytes = obj.description.encode("utf-8")
#                 description_bytes = base64.b64decode(base64_bytes)
#                 return description_bytes.decode("utf-8")
#             except (binascii.Error, UnicodeDecodeError):
#                 return "Invalid base64 data"
#         return None
        
        
        
        
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