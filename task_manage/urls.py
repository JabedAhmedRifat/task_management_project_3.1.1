from .views import *
from django.urls import path
from .postviews import *


urlpatterns = [
    path('task-create/', createTaskView),
    path('task-list/', allTaskView),
    path('task-detail/<int:pk>/', detailTaskView),
    path('task-update/<int:pk>/', updateTaskView),
    path('task-delete/<int:pk>/', deleteTaskView),
    
    
    path('user-task-detail/<int:pk>/', userDetailView),
    
    
    
    
    path('task-history-create/', CreateTaskHistoryView),
    path('task-history-list/', allTaskHistoryView),
    path('task-history-detail/<int:pk>/', detailTaskHistoryView),
    path('task-history-update/<int:pk>/', updateTaskHistoryView),
    path('task-history-delete/<int:pk>/', deleteTaskHistoryView),
    
    
    path('notice-create/', createNoticeView),
    path('notice-list/', allNoticeView),
    path('notice-detail/<int:pk>/', detailNoticeView),
    path('notice-update/<int:pk>/', updateNoticeView),
    path('notice-delete/<int:pk>/', deleteNoticeView),
    
    
    path('notificaiton-list/', allNotificationView),
    
    
    
    path('option-list/', allCheckListOptionView),
    path('option-create/', createCheckListOptionView),
    path('option-delete/<int:pk>/', deleteCheckListOptionView),
    
    
    # path('qc-user/', allQCUserListView),
    # path('qc-update/<int:pk>/', updateQC),
    # path('qc-detail/<int:pk>/', detailQCUser),
    
    
    # path('my-task-list/', qcCheckTasksView),
    
    
    path('qc-status-list/', listQcStatus),
    path('qc-status-detail/<int:pk>/', detailQcStatus),
    path('qc-status-create/', createQcStaus),
    path('qc-status-update/<int:pk>/', updateQcStatus),
    path('qc-status-delete/<int:pk>/', deleteQcStatus),
    
    
    path('qc-task-list/', listQcTask),
    path('qc-task-detail/<int:pk>/', detailQcTask),
    path('qc-task-create/', createQcTask),
    path('qc-task-update/<int:pk>/', updateQcTask),
    path('qc-task-delete/<int:pk>/', deleteQcTask),
    
    
    
    #filter
    path('search-task/', searchTaskInQcTask.as_view()),
    path('search-qc/', searchQcInQCStatus.as_view()),
    path('search-user-for-qc/', searchUserInQcTask.as_view()),
    
    # path('user-task-list/', qcTaskList),
]
