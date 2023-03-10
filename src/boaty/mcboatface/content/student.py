# -*- coding: utf-8 -*-
from boaty.mcboatface import _
from plone.app.textfield import RichText

from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset

# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from boaty.mcboatface.browser.widgets.widget_rating import RatingFieldWidget

vocab_gender = SimpleVocabulary(
    [
        # SimpleTerm(value='--NOVALUE--', title=_(u'Please Select')),
        SimpleTerm(value="male", title=_("Male")),
        SimpleTerm(value="female", title=_("Female")),
        SimpleTerm(value="doNotWantToMention", title=_("Do not want to mention")),
    ]
)


class IStudent(model.Schema):
    """Marker interface and Dexterity Python Schema for Student"""
    firstName = schema.TextLine(title=_("First name"), required=True)
    lastName = schema.TextLine(title=_("Last name"), required=True)

    directives.widget(studentRating=RatingFieldWidget)
    studentRating = schema.Float(title=_("Rating"), required=False)

    directives.widget(studentLikes=RatingFieldWidget)
    studentLikes = schema.Float(title=_("Likes"), required=False)
    studentLikes.rate_or_like='like'

    studentName = schema.TextLine(title=_("Name of student"), required=True)

    age = schema.TextLine(title=_("Age of student"), required=False)

    gender = schema.Choice(title=_("Gender"), vocabulary=vocab_gender)

    married = schema.Choice(title=_("Are you married?"), vocabulary="yes_no_dont_know")
    
    directives.widget(demofield=CheckBoxFieldWidget)
    demofield = schema.List(
        title=_(u"demofield"),
        required=False,
        description=_(u''),
        value_type=schema.Choice(vocabulary="yes_no_dont_know")
    )

    listnormal = schema.List(
       title=u'List Field',
       value_type=schema.Choice(vocabulary="yes_no_dont_know")
    )

    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('student.xml')

    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    text = RichText(title=_("Text"), required=False)

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    studentPhoto = namedfile.NamedBlobImage(
        title=_("Student photo"),
        required=False,
    )

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )

    fieldset("Photos", fields=["studentPhoto"])
    fieldset("Bio", fields=["text"])

    @invariant
    def validateNumber(data):
        # import pdb;pdb.set_trace()
        if data.age:
            if not str(data.age).isdigit():
                raise Invalid(_("Age of student must be number"))
            else:
                if int(data.age) > 110:
                    raise Invalid(_("Age of student can not be more than 110"))


@implementer(IStudent)
class Student(Item):
    """Content-type class for IStudent"""

    def Title(self):
        if self.firstName and self.lastName:
            return self.firstName + ' ' + self.lastName
        return self.studentName

    def ageBelow25(self):
        if self.age:
            if int(self.age) < 25:
                return 'yes'
            else:
                return 'no'
        return None