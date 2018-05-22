from django.urls import reverse


def test_set_homepage_content(client, site_settings):
    site_settings.homepage_content = '<b>hello world</b>'
    site_settings.save()

    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert site_settings.homepage_content in response.content.decode()
