# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Item

from plone.namedfile import field as namedfile
from plone.supermodel import model

from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


from boaty.mcboatface import _

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
# from zope.interface import invariant, Invalid

vocab_gender = SimpleVocabulary([
    # SimpleTerm(value='--NOVALUE--', title=_(u'Please Select')),
    SimpleTerm(value='male', title=_(u'Male')),
    SimpleTerm(value='female', title=_(u'Female')),
    SimpleTerm(value='doNotWantToMention', title=_(u'Do not want to mention')),
])



class IStudent(model.Schema):
    """Marker interface and Dexterity Python Schema for Student"""

    studentName = schema.TextLine(
        title=_(u'Name of student'),
        required=True
    )
    
    age = schema.TextLine(
        title=_(u'Age of student')
    )

    gender = schema.Choice(
        title=_(u'Gender'),
        vocabulary=vocab_gender
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

    text = RichText(
         title=_(u'Text'),
         required=False
    )

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    fieldset('Photos', fields=['studentPhoto'])
    studentPhoto = namedfile.NamedBlobImage(
         title=_(u'Student photo'),
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


@implementer(IStudent)
class Student(Item):
    """Content-type class for IStudent"""
