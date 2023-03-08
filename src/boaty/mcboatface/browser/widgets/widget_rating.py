__docformat__ = "reStructuredText"
import zope.component
import zope.interface
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form.widget import Widget, FieldWidget
from z3c.form.browser import widget


import logging

logger = logging.getLogger(
    "boaty.mcboatface.widgets.widget_rating.py")


class IRatingFormatWidget(interfaces.ITextWidget):
    pass

@zope.interface.implementer_only(IRatingFormatWidget)
class RatingWidget(widget.HTMLTextInputWidget, Widget):
    """Input type text widget implementation."""

    klass = u'rating-widget'
    css = u'text'
    value = None
    rate_or_like = 'rate'

    def update(self):
        super(RatingWidget, self).update()
        widget.addFieldClass(self)

        if getattr(self.field,'rate_or_like',None):
            self.rate_or_like = getattr(self.field,'rate_or_like')

        # add_resource_on_request(
        #    self.request,
        #    'customlabel-edit-style')
        # import pdb;pdb.set_trace()
        # logger.info('customlabel-edit-style applied')


@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def RatingFieldWidget(field, request):
    """IFieldWidget factory for TextWidget."""
    return FieldWidget(field, RatingWidget(request))
