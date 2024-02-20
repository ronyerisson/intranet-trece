from plone.dexterity.content import Container
from plone.supermodel.model import Schema
from zope import schema
from zope.interface import implementer


class IArea(Schema):
    """Definição de uma Área no TRE-CE."""

    # Informações básicas
    title = schema.TextLine(title="Nome da Área", required=True)
    description = schema.Text(title="Descrição", required=False)

    # Contato
    email = schema.TextLine(title="E-mail", required=True)
    ramal = schema.TextLine(title="Ramal", required=True)


@implementer(IArea)
class Area(Container):
    """Área no TRE-CE."""
