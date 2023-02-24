from zope.interface import Interface
from zope import schema
from z3c.form import form, button, field
from plone.z3cform import layout
import logging

logger = logging.getLogger('customform')


class IMyFormSchema(Interface):
    field1 = schema.TextLine(title=u"A text example field")
    field2 = schema.Int(title=u"An integer example field")


class AddNewTask(form.Form):
    schema = IMyFormSchema
    ignoreContext = True
    fields = field.Fields(IMyFormSchema)

    @button.buttonAndHandler(u'Submit')
    def handleApply(self, action):
        data, errors = self.extractData()
        logger.info(data)
        logger.info(errors)
        # do something

AddNewTaskView = layout.wrap_form(AddNewTask)
