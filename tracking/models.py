from __future__ import unicode_literals
import logging

from django.dispatch import Signal, receiver
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.conf import settings

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, default='')
    related_content_type = models.ForeignKey(ContentType, null=True, blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('related_content_type', 'related_object_id')
    
    class Meta:
        ordering = ('-timestamp',)
        get_latest_by = 'timestamp'
        app_label = 'tracking'
    
    def __unicode__(self):
        return "%s at %s" % ( self.name, self.timestamp )
    
    @classmethod
    def events_related_to(cls, related_object):
        related_ct = ContentType.objects.get_for_model(related_object)
        related_pk = related_object.id
        
        return Event.objects.filter(related_content_type=related_ct,
                                    related_object_id=related_pk)
    

event_logged = Signal(providing_args=["event"])

@receiver(models.signals.post_save, sender=Event)
def event_handler(sender, instance, created=False, **kwargs):
    if instance is not None and created:
        event_logged.send_robust(sender=sender, event=instance)

# logging callback
@receiver(event_logged)
def event_logger(sender, event=None, **kwargs):
    if event is not None:
        extra = dict(note=event.note, timestamp=event.timestamp,
            user=None, related_object=None, request=None)
        msg = ['%s event created' % event.name]
        if event.user is not None:
            extra['user'] = event.user.username
            msg.append('for user %s' % event.user.username)
        if event.related_object is not None:
            extra['related_object'] = event.related_object
            msg.append('connected to %r' % event.related_object)
        if hasattr(event, 'request') and event.request is not None:
            extra['request'] = event.request
            msg.append('@ %s' % event.request.path)
        logger.info(' '.join(msg), extra=extra)
