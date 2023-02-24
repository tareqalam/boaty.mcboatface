from zope.interface import Interface
from zope import schema
from z3c.form import form, button, field
from plone.z3cform import layout
import logging
from plone import api
from boaty.mcboatface.database import get_connection

logger = logging.getLogger('customform')


class IMyFormSchema(Interface):
    email = schema.TextLine(title=u"Email")
    password = schema.Password(title=u"Password")
    age = schema.TextLine(title=u"Age of student", required=False)



class AddNewUser(form.Form):
    schema = IMyFormSchema
    ignoreContext = True
    fields = field.Fields(IMyFormSchema)

    @button.buttonAndHandler(u'Submit me')
    def handleApply(self, action):
        data, errors = self.extractData()
        # send data in email
        # register user in plone
        # register an ScholarshipApplication content type with data

        logger.info(data)
        logger.info(errors)
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, (data.get('email'), data.get('password')))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                logger.info(result)
                # do something
            api.portal.show_message(message='Success!', request=self.request)

AddNewUserView = layout.wrap_form(AddNewUser)
