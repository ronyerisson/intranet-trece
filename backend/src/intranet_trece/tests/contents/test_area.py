from intranet_trece.content.area import Area
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import pytest


CONTENT_TYPE = "Area"


@pytest.fixture
def payload() -> dict:
    """Payload to create a new Area."""
    return {
        "type": CONTENT_TYPE,
        "title": "Alex Limi",
        "description": "Criador do Plone",
        "email": "limi@plone.org",
        "ramal": "1975",
        "id": "alex-limi",
    }


class TestArea:
    @pytest.fixture(autouse=True)
    def _fti(self, get_fti, integration):
        self.fti = get_fti(CONTENT_TYPE)

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Area)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.versioning",
            "intranet_trece.contact_info",
        ],
    )
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    @pytest.mark.parametrize(
        "roles",
        [
            ["Manager"],
            ["Editor"],
            ["Contributor"],
            ["Site Administrator"],
        ]
    )
    def test_cant_create_outsite_estrutura(self, portal, payload, roles):
        from AccessControl.unauthorized import Unauthorized

        with pytest.raises(Unauthorized) as exc:
            with api.env.adopt_roles(roles):
                api.content.create(container=portal, **payload)
        assert "Cannot create Area" in str(exc)

    @pytest.mark.parametrize(
        "roles",
        [
            ["Manager"],
            ["Editor"],
            ["Contributor"],
            ["Site Administrator"],
        ]
    )
    def test_create_inside_estrutura(self, portal, payload, roles):
        container = portal["estrutura"]
        with api.env.adopt_roles(roles):
            content = api.content.create(container=container, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Area)

    def test_review_state(self, portal, payload):
        container = portal["estrutura"]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=container, **payload)
        assert api.content.get_state(content) == "internal"

    def test_transition_editor_cannot_publish_internally(self, portal, payload):
        container = portal["estrutura"]
        with api.env.adopt_roles(["Editor"]):
            content = api.content.create(container=container, **payload)
            with pytest.raises(api.exc.InvalidParameterError) as exc:
                api.content.transition(content, "publish_internally")
        assert api.content.get_state(content) == "internal"


    def test_subscriber_added_with_description_value(self, portal):
        container = portal["estrutura"]
        with api.env.adopt_roles(["Manager"]):
            area = api.content.create(
                container=container,
                type=CONTENT_TYPE,
                title="Comunicação",
                description="Área de Comunicação",
                email="secom@tre-ce.jus.br",
                tipo_email="corporativo",
                ramal="2022",
            )
        assert area.exclude_from_nav is False

    def test_subscriber_added_without_description_value(self, portal):
        container = portal["estrutura"]
        with api.env.adopt_roles(["Manager"]):
            area = api.content.create(
                container=container,
                type=CONTENT_TYPE,
                title="Comunicação",
                description="",
                email="secom@tre-ce.jus.br",
                ramal="2022",
            )
        assert area.exclude_from_nav is True

    def test_subscriber_modified(self, portal):
        container = portal["estrutura"]
        with api.env.adopt_roles(["Manager"]):
            area = api.content.create(
                container=container,
                type=CONTENT_TYPE,
                title="Comunicação",
                description="",
                email="secom@tre-ce.jus.br",
                ramal="2022",
            )
        assert area.exclude_from_nav is True

        with api.env.adopt_roles(["Manager"]):
            area.description="Comunicação"
            notify(ObjectModifiedEvent(area))
        assert area.exclude_from_nav is False


