# -*- coding: utf-8 -*-

from plone import api
from Products.Five.browser import BrowserView
from AccessControl import Unauthorized

from Products.CMFPlone.interfaces import IRedirectAfterLogin
from zope.component import getGlobalSiteManager
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces import IRequest
import logging
logger = logging.getLogger("boaty.mcboatface.login_redirect")

@implementer(IRedirectAfterLogin)
class AfterLoginAdapter(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, came_from=None, is_first_login=False):
        return self.context.absolute_url() + '/login_next'


gsm = getGlobalSiteManager()
gsm.registerAdapter(AfterLoginAdapter,
                    (Interface, IRequest))


class LoginNext(BrowserView):

    def __call__(self):
        if api.user.is_anonymous():
            raise Unauthorized
        user = api.user.get_current()
        # groups = api.group.get_groups(username=user.getId())
        # groupnames = [localgroup.getGroupName() for localgroup in groups]
        roles = api.user.get_roles(user=user)
        if 'Manager' in roles:
            return self.context.REQUEST.RESPONSE.redirect(self.context.portal_url() + '/folder_contents')
        if 'Student' in roles:
            return self.context.REQUEST.RESPONSE.redirect(self.context.portal_url() + '/student_dashboard')
        departments = api.content.find(portal_type='Department')
        if len(departments) > 0:
            return self.context.REQUEST.RESPONSE.redirect(self.context.portal_url() + departments[0].getPath() + '/')
            # return self.context.REQUEST.RESPONSE.redirect(self.context.portal_url() + '/folder_contents')
        return self.context.REQUEST.RESPONSE.redirect(self.context.portal_url())
