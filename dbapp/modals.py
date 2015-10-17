from .forms import create_dbapp_form
from core.modals import Modal
from django.contrib.auth import get_user_model

_user = get_user_model()

class BaseDbModal(Modal):

    def create_form(self):
        self.form = create_dbapp_form(self.id, self.request.POST, self.form_name)


class DbactionModal(BaseDbModal):

    def before_save(self):
        request = self.request
        user_instance = _user.objects.get(email=request.user)
        instance = self.form.instance
        instance.user = user_instance
        instance.execute_status = 0
        
    
