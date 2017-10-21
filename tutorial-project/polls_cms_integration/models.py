from django.db import models
from cms.models import CMSPlugin
from polls.models import Poll

# Create your models here.
class PollPluginModel(CMSPlugin):
    poll = models.ForeignKey(Poll)

    def __unicode__(self):
        return self.poll.question
