from plone import api

class TestPortalProperties:

    def test_portal_title(self,portal):
        expected="Intranet TRE-CE"
        value= api.portal.get_registry_record("plone.site_title")
        assert value==expected, f"Value '{}' is not equal '{expected}'"