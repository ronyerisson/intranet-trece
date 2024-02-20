from plone import api


class TestPortalProperties:

    def test_portal_title(self, portal):
        expected = "Nova Intranet TRE-CE"
        value = api.portal.get_registry_record("plone.site_title")
        assert value == expected, f"Value '{value}' is not equal '{expected}'"

    def test_portal_timezone(self, portal):
        expected = "America/Fortaleza"
        value = api.portal.get_registry_record("plone.portal_timezone")
        assert value == expected, f"Value '{value}' is not equal '{expected}'"

    def test_portal_sitemap(self, portal):
        expected = True
        value = api.portal.get_registry_record("plone.enable_sitemap")
        assert value is expected, f"Value '{value}' is not '{expected}'"

    def test_portal_email_from_name(self, portal):
        expected = "Nova Intranet TRE-CE"
        value = api.portal.get_registry_record("plone.email_from_name")
        assert value == expected, f"Value '{value}' is not equal '{expected}'"
