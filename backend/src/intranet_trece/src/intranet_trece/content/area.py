from intranet_trece import _
from intranet_trece import validadores
from plone.dexterity.content import Container
from plone.schema.email import Email
from plone.supermodel import model
from plone.supermodel.model import Schema
from zope import schema
from zope.interface import implementer


class IArea(Schema):
    """Definição de uma Área no TRE-CE."""

    title = schema.TextLine(title=_("Nome da Área"), required=True)
    description = schema.Text(title=_("Descrição"), required=False)

    model.fieldset(
        "contato",
        _("Contato"),
        fields=[
            "email",
            "ramal",
        ],
    )
    email = Email(
        title=_("Email"),
        required=True,
        constraint=validadores.is_valid_email,
    )
    ramal = schema.TextLine(
        title=("Ramal"),
        required=True,
        constraint=validadores.is_valid_extension,
    )


@implementer(IArea)
class Area(Container):
    """Área no TRE-CE."""
