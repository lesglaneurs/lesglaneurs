import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Project, Address, Event

class PagesTests(TestCase):

    def test_map_page(self):
        response = self.client.get(reverse('map'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('mapid' in response.content, True)

    def test_map_addresses(self):
        self.empty_db()
        response = self.client.get(reverse('map_events'))
        self.assertEqual(200, response.status_code)
        self.populate_db_with_small_data()
        response = self.client.get(reverse('map_addresses'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)['addresses']), 3)

    def test_map_events(self):
        self.empty_db()
        response = self.client.get(reverse('map_events'))
        self.assertEqual(200, response.status_code)
        self.populate_db_with_small_data()
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

    def populate_db_with_small_data(self):
        response = self.client.get(reverse('populate_db_with_small_data'))
        self.assertEqual(200, response.status_code)

        self.assertEqual(len(Project.objects.all()), 3)

        addresses = Address.objects.all()
        self.assertEqual(len(addresses), 3)
        for address in addresses:
            self.assertEqual(len(address.events.all()), 1)

        events = Event.objects.all()
        self.assertEqual(len(events), 3)
        for event in events:
            self.assertEqual(isinstance(event.project, Project), True)

    def empty_db(self):
        response = self.client.get(reverse('empty_db'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(Project.objects.all()), 0)
        self.assertEqual(len(Address.objects.all()), 0)
        self.assertEqual(len(Event.objects.all()), 0)
