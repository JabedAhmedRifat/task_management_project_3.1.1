from rest_framework import serializers
from .models import *



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
    class Meta:
        model = Task
        fields = '__all__'
        
        
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