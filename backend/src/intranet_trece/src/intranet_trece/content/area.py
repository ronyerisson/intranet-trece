from intranet_trece import _
from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.dexterity.content import Container
from plone.schema.email import Email
from plone.supermodel import model
from plone.supermodel.model import Schema
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer

import re


def is_valid_email(value: str) -> bool:
    """Validar se o email é @tre-ce.jus.br."""
    return value.endswith("@tre-ce.jus.br") if value else True


def is_valid_extension(value: str) -> bool:
    """Validar se o o ramal tem 4 dígitos numéricos."""
    return re.match(r"^\d{4}$", value) if value else True


class IArea(Schema):
    """Definição de uma Área no TRE-CE."""

    # Informações básicas
    title = schema.TextLine(title="Nome da Área", required=True)
    description = schema.Text(title="Descrição", required=False)

    # Contato
    email = schema.TextLine(title="E-mail", required=True)
    ramal = schema.TextLine(title="Ramal", required=True)

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
        required=False,
        constraint=is_valid_email,
    )
    ramal = schema.TextLine(
        title=("Ramal"),
        required=False,
        constraint=is_valid_extension,
    )


@implementer(IArea)
class Area(Container):
    """Área no TRE-CE."""
