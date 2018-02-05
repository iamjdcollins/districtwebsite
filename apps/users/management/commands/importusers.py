from django.conf import settings
from django.db.models import Q
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from ldap3 import Connection, Server, ANONYMOUS, SIMPLE, SYNC, ASYNC, ALL, NTLM
from apps.users.models import Employee, System
from apps.objects.models import Node
from django.contrib.auth.models import Group
import uuid

def show_in_directory(item,obj):
    exclude_upn = [
        'webmaster@slcschools.org',
    ]
    exclude_department = [
        'substitute teachers',
    ]

    if str(item.userPrincipalName).lower() in  exclude_upn:
        return False
    if str(item.department).lower() in exclude_department:
        return False
    if obj.non_employee:
        return False
    return True

def job_title_titlecase(item):
    overwrite_titlecase = {
    
    }
    if str(item.title).lower() == '[]':
        return ''
    if str(item.title).lower() in overwrite_titlecase:
        return overwrite_titlecase[str(item.title).lower()]
    return str(item.title)

def directory_department(item,departments):
    if str(item.department).lower() in departments:
        return departments[str(item.department).lower()]
    return None

def importUser(item, account, departments,all_adult_staff,website_managers):
  site = Site.objects.get(domain='www.slcschools.org')
  obj, created = Employee.objects.get_or_create(uuid=uuid.UUID(str(item.objectGUID)), defaults={'email':'tempemail@slcschools.org','url':'/tempemail', 'site': site  })
  obj.username = str(item.userPrincipalName).lower()
  obj.first_name = item.givenName
  obj.last_name = item.sn
  if item.mail:
    obj.email = str(item.mail).lower()
  else:
    obj.email = str(item.userPrincipalName).lower()
  obj.job_title = job_title_titlecase(item)
  obj.department = directory_department(item,departments)
  obj.is_staff = True
  if str(item.extensionAttribute1).lower().startswith('n-'):
    obj.non_employee = True
  else:
    obj.non_employee = False
  obj.in_directory = show_in_directory(item,obj)
  obj.deleted = False
  if created:
    obj.create_user = account
  obj.update_user = account
  obj.groups.add(all_adult_staff)
  if 'CN=USR_SERVERS_WEB_MANAGERS,OU=WEB,OU=SERVERS,DC=SLCSD,DC=NET' in item.memberOf.values:
      obj.groups.add(website_managers)
  obj.save()

class Command(BaseCommand):
  def handle(self, *args, **options):
    department_nodes = Node.objects.filter(deleted=0).filter(published=1).filter(Q(content_type='school') | Q(content_type='department')).order_by('node_title')
    departments = {}
    for node in department_nodes:
      departments[str(node.node_title).lower()] = node
    importuserssvc = System.objects.get(username='importuserssvc')
    all_adult_staff = Group.objects.get(name='All Adult Staff')
    website_managers = Group.objects.get(name='Website Managers')
    server = Server('slcsd.net', use_ssl=True, get_info=ALL)
    conn = Connection(server, user=settings.SLCSD_LDAP_USER, password=settings.SLCSD_LDAP_PASSWORD, authentication=NTLM)
    conn.bind()
    conn.search('OU=WEB,OU=SERVERS,DC=SLCSD,DC=NET', '(&(objectClass=user)(| (memberof:1.2.840.113556.1.4.1941:=CN=USR_SERVERS_WEB_ALL_ADULT_STAFF,OU=WEB,OU=SERVERS,DC=SLCSD,DC=NET)(memberof:1.2.840.113556.1.4.1941:=CN=USR_SLCSD_NONEMPLOYEE,DC=SLCSD,DC=NET)))', attributes=['DisplayName','userPrincipalName','givenName','sn','objectGUID','mail','department','title','extensionAttribute1','memberOf',])
    for item in conn.entries:
      importUser(item, importuserssvc,departments,all_adult_staff,website_managers)
    conn.search('OU=DO,DC=SLCSD,DC=NET', '(&(objectClass=user)(| (memberof:1.2.840.113556.1.4.1941:=CN=USR_SERVERS_WEB_ALL_ADULT_STAFF,OU=WEB,OU=SERVERS,DC=SLCSD,DC=NET)(memberof:1.2.840.113556.1.4.1941:=CN=USR_SLCSD_NONEMPLOYEE,DC=SLCSD,DC=NET)))', attributes=['DisplayName','userPrincipalName','givenName','sn','objectGUID','mail','department','title','extensionAttribute1','memberOf',])
    for item in conn.entries:
      importUser(item, importuserssvc,departments,all_adult_staff,website_managers)
    conn.search('OU=INFORMATION_SYSTEMS,DC=SLCSD,DC=NET', '(&(objectClass=user)(|(memberof:1.2.840.113556.1.4.1941:=CN=USR_SERVERS_WEB_ALL_ADULT_STAFF,OU=WEB,OU=SERVERS,DC=SLCSD,DC=NET)(memberof:1.2.840.113556.1.4.1941:=CN=USR_SLCSD_NONEMPLOYEE,DC=SLCSD,DC=NET)))', attributes=['DisplayName','userPrincipalName','givenName','sn','objectGUID','mail','department','title','extensionAttribute1','memberOf',])
    for item in conn.entries:
      importUser(item, importuserssvc,departments,all_adult_staff,website_managers)
