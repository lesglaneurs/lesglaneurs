import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Project, Address, Event
from .views import get_departments, get_projects, get_months

class PagesTests(TestCase):

    def test_map_page(self):
        response = self.client.get(reverse('map'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('mapid' in response.content, True)

    def test_map_addresses(self):
        self.load_small_data()
        response = self.client.get(reverse('map_addresses'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)['addresses']), 3)

    def test_map_events(self):
        self.load_small_data()
        response = self.client.get(reverse('map_events'))
        self.assertEqual(200, response.status_code)
        events = json.loads(response.content)['events']
        self.assertEqual(len(events), 3)
        for event in events:
            project_name = event['project']['fields']['name']
            self.assertEqual(project_name.startswith('Association'), True)
            addresses = event['addresses']
            for address in addresses:
                self.assertEqual(address['fields']['country'], 'France')

    def load_small_data(self):
        response = self.client.get(reverse('load_small_data'))
        self.assertEqual(200, response.status_code)

        self.assertEqual(len(Project.objects.all()), 3)

        addresses = Address.objects.all()
        self.assertEqual(len(addresses), 3)

        events = Event.objects.all()
        self.assertEqual(len(events), 3)
        for event in events:
            self.assertEqual(isinstance(event.project, Project), True)
            self.assertEqual(len(event.addresses.all()), 1)

    def test_empty_db(self):
        response = self.client.get(reverse('empty_db'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(Project.objects.all()), 0)
        self.assertEqual(len(Address.objects.all()), 0)
        self.assertEqual(len(Event.objects.all()), 0)

    def test_get_departments(self):
        self.client.get(reverse('load_small_data'))
        self.assertEqual(get_departments(),  ['Tous', '27', '33', '75'])

    def test_get_projects(self):
        self.client.get(reverse('load_small_data'))
        expected = ['Tous',
                    'Association de Guiseniers',
                    'Association de Paris',
                    "Association de Saint-Pierre d'Aurillac"]
        self.assertEqual(get_projects(),  expected)

    def test_get_months(self):
        expected =  ['Tous', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.assertEqual(get_months(), expected)
