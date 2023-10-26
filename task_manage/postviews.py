from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from knox.auth import TokenAuthentication

from django.contrib.auth.models import User
from user.models import UserProfile



# Create your views here.
from .models import *
from .serializers import *







@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def createCheckListOptionView(request):
    data = request.data
    serializer = CheckListSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
    
    
    
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def deleteCheckListOptionView(request,pk):
    data = CheckListOption.objects.get(id=pk)
    data.delete()
    return Response({"message":"deleted"})
    





@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def createTaskView(request):
    data = request.data
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.type == 'superadmin' or user_profile.type == 'admin':
            serializer = TaskSerializer(data=data)
            if serializer.is_valid():
                serializer.save()


                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'error': 'Only super admin and admins can create Task'})

    except UserProfile.DoesNotExist:
        return Response({'error': 'User Profile does not exist'})






@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def updateTaskView(request, pk):
    user = request.user
    data = request.data
    try:
        user_profile = UserProfile.objects.get(user=user)
        task = Task.objects.get(id=pk)

        if user_profile.type in ['superadmin']:
            serializer = TaskSerializer(instance=task, data=data, partial=True)

            if serializer.is_valid():
                if 'status' in data and task.status == 'qc_complete' and data['status'] == 'done':
                    task.assignee.score += task.points
                    task.assignee.save()
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
            



        elif user_profile.type == 'admin' and task.assigner == user_profile:
            serializer = TaskSerializer(instance=task, data=data, partial=True)
            if serializer.is_valid():
                if 'status' in data and task.status == 'qc_complete' and data['status'] == 'done':
                    task.assignee.score += task.points
                    task.assignee.save()
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)





        elif user_profile.type == 'member' and task.assignee == user_profile:
            allowed_status = ['todo', 'inprogress', 'checklist', 'pause']
            if 'status' in data:
                if data['status'] not in allowed_status:
                    return Response({"error": "Member can only set status to 'Todo', 'In Progress', 'Checklist', 'Pause'"})

            
            
            update_data = {}
            
            fields_to_update = ['status', 'task_submit']

            for field in fields_to_update:
                if field in data:
                    update_data[field] = data[field]

            serializer = TaskSerializer(instance=task, data=update_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Status updated", "data": serializer.data})
            
            
            else:
                return Response({"message": "only Status and Task Submit can be updated by assignee User"})


        elif QCTask.objects.filter(task=task, user=user_profile).exists():
            allowed_status = ['inprogress', 'qc_complete', 'qc_progress']
            if 'status' in data:
                if data['status'] not in allowed_status:
                    return Response({"message": "QC user only set status to  'InProgress' or qc_complete, qc_progress"})
                    
            update_data = {'status': data.get('status')}

            serializer = TaskSerializer(instance=task, data = update_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "status update", "data" : serializer.data})
            else:
                return Response({"message": "qc checker only update status"})



        else:
            return Response({'error': 'Permission denied'})


    except UserProfile.DoesNotExist:
        return Response({'errors': 'User profile does not exist'})
    except Task.DoesNotExist:
        return Response({'errors': 'Task does not exist'})




#___________________QC Status____________________________________________


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def createQcStaus(reqeust):
    data = reqeust.data
    serializer = QCStatusSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def updateQcStatus(request,pk):
    status = QCStatus.objects.get(id=pk)
    data = request.data
    serializer = QCStatusSerializer(instance=status, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)




# ______________________QC Task_____________________________________________



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def createQcTask(reqeust):
    data = reqeust.data
    serializer = QCTaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def updateQcTask(request,pk):
    status = QCTask.objects.get(id=pk)
    data = request.data
    serializer = QCTaskSerializer(instance=status, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    






#_______________Task History________________________________________________ 


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def CreateTaskHistoryView(request):
    data = request.data
    serializer = TaskHistorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)





@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def updateTaskHistoryView(request,pk):
    taskHistory= TaskHistory.objects.get(id=pk)
    data = request.data 
    serializer = TaskSerializer(instance=taskHistory, data = data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)













#_____________________Notice___________________________________________

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def createNoticeView(request):
    data = request.data 
    user = request.user
    
    try:
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.type in ['superadmin', 'admin']:
            serializer = NoticeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return(serializer.errors)
        
        else:
            return Response({'error':'Only SuperAdmin and Admin can CreateNotice'})
        
    except UserProfile.DoesNotExist:
        return Response({'error': 'User Profile Does Not Exist'})
                



















@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def updateNoticeView(request,pk):
    user = request.user
    data = request.data 
    
    try:
        user_profile = UserProfile.objects.get(user=user)
        notice = Notice.objects.get(id=pk)
        
        if user_profile.type in ['superadmin', 'admin']:
            serializer = NoticeSerializer(instance=notice, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        
        else:
            return Response({'error':'Super admin and admin only can update Notice'})
        
        
    except UserProfile.DoesNotExist:
        return Response({'error':'User Profile Does not exist'})
    
    

