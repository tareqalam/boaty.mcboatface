# -*- coding: utf-8 -*-
from __future__ import absolute_import

from Acquisition import aq_inner
from boaty.mcboatface import _
from plone import schema
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope.component import getMultiAdapter
from zope.interface import implementer

import json
import six.moves.urllib.error
import six.moves.urllib.parse
import six.moves.urllib.request


class IBoatyportletPortlet(IPortletDataProvider):
    place_str = schema.TextLine(
        title=_("Name of your place with country code"),
        description=_("City name along with country code i.e Delhi,IN"),  # NOQA: E501
        required=True,
        default="delhi,in",
    )


@implementer(IBoatyportletPortlet)
class Assignment(base.Assignment):
    schema = IBoatyportletPortlet

    def __init__(self, place_str="delhi,in"):
        self.place_str = place_str.lower()

    @property
    def title(self):
        return _("Weather of the place")


class AddForm(base.AddForm):
    schema = IBoatyportletPortlet
    form_fields = field.Fields(IBoatyportletPortlet)
    label = _("Add Place weather")
    description = _("This portlet displays weather of the place.")

    def create(self, data):
        return Assignment(
            place_str=data.get("place_str", "delhi,in"),
        )


class EditForm(base.EditForm):
    schema = IBoatyportletPortlet
    form_fields = field.Fields(IBoatyportletPortlet)
    label = _("Edit Place weather")
    description = _("This portlet displays weather of the place.")


class Renderer(base.Renderer):
    schema = IBoatyportletPortlet
    _template = ViewPageTemplateFile("boatyportlet.pt")

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter(
            (context, self.request), name="plone_portal_state"
        )
        self.anonymous = portal_state.anonymous()

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements and
        not an anonymous user."""
        return not self.anonymous and self._data()

    def weather_report(self):
        self.result = self._data()
        return self.result["description"]

    def get_humidity(self):
        return self.result["humidity"]

    def get_pressure(self):
        return self.result["pressure"]

    @memoize
    def _data(self):
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="{0}")'.format(  # NOQA: E501
            self.data.place_str,
        )
        yql_url = (
            baseurl
            + six.moves.urllib.parse.urlencode(
                {"q": yql_query},
            )
            + "&format=json"
        )
        result = six.moves.urllib.request.urlopen(yql_url).read()
        data = json.loads(result)
        result = {}
        result["description"] = data["query"]["results"]["channel"][
            "description"
        ]  # NOQA: E501
        result["pressure"] = data["query"]["results"]["channel"]["atmosphere"][
            "pressure"
        ]  # NOQA: E501
        result["humidity"] = data["query"]["results"]["channel"]["atmosphere"][
            "humidity"
        ]  # NOQA: E501
        return result
