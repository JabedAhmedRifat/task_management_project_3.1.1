from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from knox.auth import TokenAuthentication

from django.contrib.auth.models import User
from user.models import UserProfile
from user.serializers import *

from django.db.models import Q

# Create your views here.
from .models import *
from .serializers import *

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics





#_______________________CheckListOption CRUD____________________




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def allCheckListOptionView(request):
    data = CheckListOption.objects.all().order_by('-id')
    serializer = CheckListSerializer(data, many=True)
    return Response(serializer.data)
        
        
        
        

# ______________________QC Task_____________________________________________


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def listQcTask(reqeust):
    qcStatus = QCTask.objects.all()
    serializer = QCTaskSerializer(qcStatus, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def detailQcTask(reqeust, pk):
    data = QCTask.objects.get(id = pk)
    serializer = QCTaskSerializer(data)
    return Response(serializer.data)





@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def deleteQcTask(request,pk):
    data = QCTask.objects.get(id=pk)
    data.delete()
    return Response({'message' : 'DELETED'})






#___________________QC Status____________________________________________



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def listQcStatus(reqeust):
    qcStatus = QCStatus.objects.all()
    serializer = QCStatusSerializer(qcStatus, many=True)
    return Response(serializer.data)





@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def detailQcStatus(reqeust, pk):
    data = QCStatus.objects.get(id = pk)
    serializer = QCStatusSerializer(data)
    return Response(serializer.data)




    

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def deleteQcStatus(request,pk):
    data = QCStatus.objects.get(id=pk)
    data.delete()
    return Response({'message' : 'DELETED'})



# ______________________Notification using signals for that_____________________________________________





@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def allNotificationView(request):
    user_profile = UserProfile.objects.get(user=request.user)

    data = Notification.objects.filter(user=user_profile).order_by('-id')
    serializer = NotificationSerializer(data, many=True)
    return Response(serializer.data)





# ________________________Task CRUD___________________________________________



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def allTaskView(request):
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
        

        if user_profile.type == 'superadmin':
            data = Task.objects.all().order_by('-id')
        elif user_profile.type == 'admin':
            data = Task.objects.all().order_by('-id')
        elif user_profile.type == 'member':
            data = Task.objects.filter(assignee=user_profile)

        elif QCTask.objects.filter(user=user_profile).exists():
            # Get tasks associated with the user as a QC task
            qc_tasks = QCTask.objects.filter(user=user_profile)
            qc_task_ids = qc_tasks.values_list('task_id', flat=True)
            data = Task.objects.filter(id__in=qc_task_ids).order_by('-id')


        serializer = TaskSerializer(data, many=True)
        return Response(serializer.data)

    except UserProfile.DoesNotExist:
        return Response({'error': 'User Profile does not exist'})








@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def detailTaskView(request, pk):
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
        data = Task.objects.get(id=pk)

        if user_profile.type == 'superadmin' or user_profile.type == 'admin':
            pass
        elif user_profile.type == 'member':
            if data.assignee == user_profile:
                pass
        

        elif QCTask.objects.filter(user=user_profile, task=data).exists():
            pass


        serializer = TaskSerializer(data)
        return Response(serializer.data)

    except UserProfile.DoesNotExist:
        return Response({'error': 'User Profile does not exist'})
    except Task.DoesNotExist:
        return Response({'error': 'Task matching Does not exist'})







@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def deleteTaskView(request,pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response({'error':'Task does not exist'})
    
    user= request.user
    user_profile = UserProfile.objects.get(user=user)

    if user_profile.type in ['superadmin', 'admin']:
        task.delete()
        return Response({'message':'Task Deleted Successfully'})
    else:
        return Response({'error':'only super admin and admin can delete tasks'})
    





# ____________________________User Detail View_______________________________________________


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def userDetailView(request, pk):
    user = request.user

    try:
        user_detail = UserProfile.objects.get(user=user)
        if user_detail.type == 'superadmin' or user_detail.type == 'admin':
            user_profile = UserProfile.objects.get(id=pk)
            user_tasks = Task.objects.filter(assignee=user_profile)
            
            # user_task_assigner = Task.objects.filter(assigner=user_profile)____________________
            
            # qc_checker_tasks = Task.objects.filter(qc_check__user=user_profile)

            user_serializer = UserProfileSerializer(user_profile)
            task_serializer = TaskSerializer(user_tasks, many=True)

            user_data = user_serializer.data
            task_data = task_serializer.data

            return Response({'user': user_data, 'tasks': task_data})
        else:
            return Response({'error': 'Permission denied. Only superadmin and admin can access this endpoint.'})

    except UserProfile.DoesNotExist:
        return Response({'error': 'User Profile does not exist'})









# ___________________________________________________________________


# QC check views

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# def qcCheckTasksView(request):
#     user = request.user

#     try:
#         user_profile = UserProfile.objects.get(user=user)

#         if user_profile:
#             # Get tasks assigned to the QC User for QC check (based on the QCUser instances)
#             qc_tasks = Task.objects.filter(qc_check__user=user_profile)

#             serializer = TaskSerializer(qc_tasks, many=True)
#             return Response(serializer.data)
#         else:
#             return Response({'error': 'Permission denied. Only QC Users can access this endpoint.'})

#     except UserProfile.DoesNotExist:
#         return Response({'error': 'User Profile does not exist'})









# ________________________Task History CRUD ___________________________________________





@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def allTaskHistoryView(request):
    user = request.user
    
    try:
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.type == 'superadmin':
            data = TaskHistory.objects.all().order_by('-id')
            
        elif user_profile.type == 'admin':
            data = TaskHistory.objects.all().order_by('-id')
            
        elif user_profile.type == 'member':
            data = TaskHistory.objects.filter(task__assignee = user_profile).order_by('-id')
            
        
        serializer = TaskHistorySerializer(data, many=True)
        return Response(serializer.data)
    
    except UserProfile.DoesNotExist:
        return Response({'error':'User Does not exist'})
        




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def detailTaskHistoryView(request,pk):
    user = request.user
    
    try:
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.type == 'superadmin':
            data = TaskHistory.objects.get(id=pk)
        elif user_profile.type == 'admin':
            data = TaskHistory.objects.get(id=pk)
        
        elif user_profile.type == 'member':
            data = TaskHistory.objects.get(task__assignee=user_profile, id=pk)
        
        serializer = TaskHistorySerializer(data)
        return Response(serializer.data)
    
    except UserProfile.DoesNotExist:
        return Response({'erro':'User with this type does not exist'})
    
        














@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def deleteTaskHistoryView(request,pk):
    data = TaskHistory.objects.get(id=pk)
    data.delete()
    return Response({'message':'Task History Deteted Successfully'})







# ____________________________Notice CRUD_______________________________________






@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def allNoticeView(request):
    data = Notice.objects.all().order_by('-id')
    serializer = NoticeSerializer(data, many=True)
    return Response(serializer.data)







@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def detailNoticeView(request,pk):
    data = Notice.objects.get(id=pk)
    serializer = NoticeSerializer(data)
    return Response(serializer.data)







@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def deleteNoticeView(request, pk):
    try:
        notice = Notice.objects.get(id=pk)
        
    except Notice.DoesNotExist:
        return Response({'error':'Notice does not exist'})
    
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    
    if user_profile.type in ['superadmin', 'admin']:
        notice.delete()
        return Response({'message':'Notice Deleted Successfully'})
    else:
        return Response({'error':'only Super Admin and admin can delele Notice'})
    
    
    
    
    
    
# ______________________Filter_____________________

class searchTaskInQcTask(generics.ListAPIView):
    queryset = QCTask.objects.all().order_by('-id')
    serializer_class = QCTaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task']
    
    
    
    
    
class searchQcInQCStatus(generics.ListAPIView):
    queryset = QCStatus.objects.all().order_by('-id')
    serializer_class = QCStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['qc']