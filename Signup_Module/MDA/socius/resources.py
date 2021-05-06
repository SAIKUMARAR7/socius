from import_export import resources
from .models import UserList

class UserListResource(resources.ModelResource):
    class Meta:
        model = UserList