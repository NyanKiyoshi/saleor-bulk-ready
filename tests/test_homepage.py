from django.urls import reverse
from django.test import Client


def test_home_with_footer_text(site_settings):
    site_settings.footer_text = 'Hello, this is the bottom.'
    site_settings.save()
    resp = Client().get(reverse('home'))
    assert resp.status_code == 200
    assert resp.content.find(site_settings.footer_text.encode('utf-8')) > 0


def test_home_without_footer_text(site_settings):
    assert not site_settings.footer_text
    resp = Client().get(reverse('home'))
    assert resp.status_code == 200
