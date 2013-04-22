""" Controller
"""
import json
from zope.component import queryAdapter
from zope.component.hooks import getSite
from eea.alchemy.controlpanel.interfaces import IAlchemySettings
from Products.Five.browser import BrowserView

class View(BrowserView):
    """ Alchemy View Controller
    """
    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self._settings = None

    @property
    def settings(self):
        """ Settings
        """
        if self._settings is None:
            site = getSite()
            self._settings = queryAdapter(site, IAlchemySettings)
        return self._settings

    def tags(self, **kwargs):
        """ Get tags
        """
        search = set()
        if getattr(self.context, 'getField', None):
            fields = self.settings.autoTaggingFields
            for name in fields:
                field = self.context.getField(name)
                if not field:
                    continue
                value = field.getAccessor(self.context)()
                if isinstance(value, (str, unicode)):
                    search.add(value)
                elif isinstance(value, (list, tuple, set)):
                    search.update(value)

        return {
            'enabled': self.settings.autoTagging,
            'link': self.settings.autoTaggingLink,
            'blacklist': self.settings.autoTaggingBlackList,
            'search': tuple(search)
        }

    def tags_json(self, **kwargs):
        """ Return self.tags as JSON
        """
        return json.dumps(self.tags(**kwargs))