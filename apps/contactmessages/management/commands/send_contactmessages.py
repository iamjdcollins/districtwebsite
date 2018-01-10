from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import apps.common.functions
from apps.contactmessages.models import ContactMessage

class Command(BaseCommand):
    def handle(self, *args, **options):
        for self in ContactMessage.objects.filter(deleted=0).filter(published=1).filter(confirm_sent=0):
            #Send Confirm Email
            print('Sending confirmation for: ' + self.message_subject + ' to ' + self.your_email)
            self.confirm_sent = apps.common.functions.contactmessage_confirm(self)
            self.save()
        for self in ContactMessage.objects.filter(deleted=0).filter(published=1).filter(message_sent=0):
            #Send Message
            print('Sending: ' + self.message_subject + ' to ' + self.primary_contact.email + ' from ' + self.your_email)
            self.message_sent = apps.common.functions.contactmessage_message(self)
            self.save()
