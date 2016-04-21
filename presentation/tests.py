from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import Project, Address, Event

class PagesTests(TestCase):

    def test_map_page(self):
        response = self.client.get(reverse('map'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('mapid' in response.content, True)

    def test_populate(self):
        response = self.client.get(reverse('populate'))
        self.assertEqual(200, response.status_code)

        self.assertEqual(len(Project.objects.all()), 3)

        addresses = Address.objects.all()
        self.assertEqual(len(addresses), 3)
        for address in addresses:
            self.assertEqual(len(address.events.all()), 1)

        self.assertEqual(len(Event.objects.all()), 3)
