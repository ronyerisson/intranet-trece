from intranet_trece import _
from plone.dexterity.content import Container
from plone.supermodel import model
from plone.supermodel.model import Schema
from zope import schema
from zope.interface import implementer


class IArea(Schema):
    """Definição de uma Área no TRE-CE."""

    title = schema.TextLine(title=_("Nome da Área"), required=True)
    description = schema.Text(title=_("Descrição"), required=False)


@implementer(IArea)
class Area(Container):
    """Área no TRE-CE."""
