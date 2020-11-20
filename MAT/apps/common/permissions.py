from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):

     """
    Custom permission to only allow owners of an object to edit it.
    """
     def has_object_permission(self, request, view, obj):
        
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user

class IsPodLeaderOrAdmin(BasePermission):
    '''
    Check if the user is a pod leader or admin before creating a cohort. 
    '''
    def has_permission(self, request, view):
        pod_leader = request.user.type =='POD_LEADER'
        admin = request.user.type =='ADMIN'
        return bool(pod_leader or admin)
