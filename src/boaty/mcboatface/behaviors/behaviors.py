from plone.app.content.interfaces import INameFromTitle
# from plone.autoform import directives
# from plone.autoform.interfaces import IFormFieldProvider
# from plone.rfc822.interfaces import IPrimaryFieldInfo
# from plone.supermodel import model
# from Products.CMFPlone.utils import safe_hasattr
# from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
# from zope.interface import provider
import datetime
# import uuid

class INameFromFirstAndLastname(Interface):
    """Marker interface to enable name from filename behavior"""


@implementer(INameFromTitle)
@adapter(INameFromFirstAndLastname)
class NameFromFirstAndLastname(object):

    def __new__(cls, context):
        first_name = str(context.firstName).replace(' ','_').lower()
        last_name = str(context.lastName).replace(' ','_').lower()
        instance = super(NameFromFirstAndLastname, cls).__new__(cls)
        if first_name and last_name:
            generated_title = '{0}-{1}'.format(first_name, last_name)
        else:
            generated_title = code

        instance.title = generated_title

        return instance

    def __init__(self, context):
        pass
