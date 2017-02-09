# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from Products.Five import BrowserView
from collective.timebank import _
from zope import schema

from plone import api
from plone.app.textfield import RichText
from z3c.relationfield import RelationChoice
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone.formwidget.contenttree import ObjPathSourceBinder
import logging

logger = logging.getLogger(__name__)


class ICollectiveTimebankLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


types = SimpleVocabulary(
        [SimpleTerm(value=u'REQUEST', title=_(u'Request')),
         SimpleTerm(value=u'OFFER', title=_(u'Offer')),]
)


class IJobTime(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )

    type = schema.Choice(
        title=_(u"Type"),
        vocabulary=types,
        required=False,
    )

    minutes_amount = schema.Int(
        title=_(u"Amount"),
        default=0,
    )


class IJobTimeBid(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )

    job = RelationChoice(
        title=_(u"Job"),
        source=ObjPathSourceBinder(object_provides=IJobTime),
        required=True,
    )


class IJobTimeSkill(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )


class IJobTimeTransaction(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    from_user = RelationChoice(
        title=_(u"From user"),
        source=ObjPathSourceBinder(),
        required=True,
    )

    to_user = RelationChoice(
        title=_(u"To user"),
        source=ObjPathSourceBinder(),
        required=True,
    )

    job = RelationChoice(
        title=_(u"Job"),
        source=ObjPathSourceBinder(object_provides=IJobTime),
        required=True,
    )

    minutes_amount = schema.Int(
        title=_(u"Amount"),
        default=0,
    )


class IJobTimeBalance(Interface):

    title = schema.TextLine(
            title=_(u"Title"),
            required=False,
    )

    minutes_balance = schema.Int(
        title=_("Balance"),
        default=0
    )


class IJobTimeBank(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )


