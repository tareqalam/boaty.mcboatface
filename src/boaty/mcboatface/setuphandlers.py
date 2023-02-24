# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from Products.CMFCore.utils import getToolByName
import logging


logger = logging.getLogger('setuphandlers')


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "boaty.mcboatface:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["boaty.mcboatface.upgrades"]


def add_catalog_indexes(context):
    """Add our indexes to the catalog.

    Doing it here instead of in profiles/default/catalog.xml means we
    do not need to reindex those indexes after every reinstall.
    inspiration from https://svn.plone.org/svn/collective/Products.Poi/trunk/Products/Poi/setuphandlers.py
    and
    http://maurits.vanrees.org/weblog/archive/2009/12/catalog
    """

    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()

    wanted_dateindex = []
    wanted_fieldindex = ["age", "gender", "ageBelow25"]
    wanted_keywordindex=()
    missing_dateindex = [w for w in wanted_dateindex if w not in indexes]
    if missing_dateindex:
        for name in missing_dateindex:
            catalog.addIndex(name, 'DateIndex')
            logger.info("Added DateIndex for field %s.", name)
        logger.info("Indexing new date indexes %s.", ', '.join(missing_dateindex))
        catalog.manage_reindexIndex(ids=missing_dateindex)

    missing_fieldindex = [w for w in wanted_fieldindex if w not in indexes]
    if missing_fieldindex:
        for name in missing_fieldindex:
            catalog.addIndex(name, 'FieldIndex')
            logger.info("Added FieldIndex for field %s.", name)
        logger.info("Indexing new field indexes %s.", ', '.join(missing_fieldindex))
        catalog.manage_reindexIndex(ids=missing_fieldindex)

    missing_keywordindex = [w for w in wanted_keywordindex if w not in indexes]
    if missing_keywordindex:
        for name in missing_keywordindex:
            catalog.addIndex(name, 'KeywordIndex')
            logger.info("Added KeywordIndex for field %s.", name)
        logger.info("Indexing new keyword indexes %s.", ', '.join(missing_keywordindex))
        catalog.manage_reindexIndex(ids=missing_keywordindex)



def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    add_catalog_indexes(context)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
