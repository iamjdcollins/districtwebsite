from ajax_select import register
import re
from apps.common.classes import UUIDLookupChannel
from apps.users.models import Employee

@register('employee')
class EmployeesLookup(UUIDLookupChannel):
  model = Employee

  def get_query(self, q, request):
    q = re.sub(' ','.*',q)
    return self.model.objects.filter(is_active=1).filter(is_staff=1).filter(in_directory=1).filter(username__iregex=q)[:10]

  def format_item_display(self, item):
    return u"<span class='employee'>%s</span>" % item.username
