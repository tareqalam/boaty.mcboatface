import zope.schema
from zope.component import adapts
from zope.interface import implementer
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import IWidget
from z3c.form.converter import FloatDataConverter
from z3c.form.converter import FormatterValidationError
from boaty.mcboatface.browser.widgets.widget_rating import IRatingFormatWidget

@implementer(IDataConverter)
class CustomRatingDataConverter(FloatDataConverter):

    adapts(zope.schema.interfaces.IFloat, IRatingFormatWidget)

    def mark(self):
        return self.formatter.symbols.get('decimal')

    def toFieldValue(self, value):
        """This will be called when we save the form"""
        if value is None:
            return None
        v = value.strip().replace(self.mark(), u'.')
        # import pdb;pdb.set_trace()
        if not len(v):
            return None
        try:
            v = float(v.replace(self.mark(), '.'))
            return v
        except ValueError:
            raise FormatterValidationError(self.errorMessage, value)

    def toWidgetValue(self, value):
        """this will be called when we laod the form"""
        # import pdb;pdb.set_trace()
        if value is self.field.missing_value or value=='':
            return u''
        return self.formatter.format(value)