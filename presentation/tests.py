import datetime
import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Project, Address, Event, Person, Membership, Role
from .views import get_departments, get_projects, get_months, get_persons, get_memberships

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

    def test_persons(self):
        self.load_small_data()
        response = self.client.get(reverse('persons'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)['persons']), 3)

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

    def test_map_events_filtered_by_month(self):
        self.load_small_data()
        month = datetime.datetime.now().month
        response = self.client.get(
            '{}?month={}'.format(reverse('map_events'), month))
        self.assertEqual(200, response.status_code)
        events = json.loads(response.content)['events']
        self.assertEqual(len(events), 3)
        month = month + 1 if month < 12 else 1
        response = self.client.get(
            '{}?month={}'.format(reverse('map_events'), month))
        self.assertEqual(200, response.status_code)
        events = json.loads(response.content)['events']
        self.assertEqual(len(events), 0)

    def test_map_events_filtered_by_project(self):
        self.load_small_data()
        project = 'Association de Guiseniers'
        response = self.client.get(
            '{}?project={}'.format(reverse('map_events'), project))
        self.assertEqual(200, response.status_code)
        events = json.loads(response.content)['events']
        self.assertEqual(len(events), 1)
        project = 'foo'
        response = self.client.get(
            '{}?project={}'.format(reverse('map_events'), project))
        self.assertEqual(200, response.status_code)
        events = json.loads(response.content)['events']
        self.assertEqual(len(events), 0)

    def test_map_events_filtered_by_department(self):
        self.load_small_data()
        department = '27'
        response = self.client.get(
            '{}?department={}'.format(reverse('map_events'), department))
        self.assertEqual(200, response.status_code)
        events = json.loads(response.content)['events']
        self.assertEqual(len(events), 1)
        department = 'foo'
        response = self.client.get(
            '{}?department={}'.format(reverse('map_events'), department))
        self.assertEqual(200, response.status_code)
        events = json.loads(response.content)['events']
        self.assertEqual(len(events), 0)

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

    def test_get_persons(self):
        self.client.get(reverse('load_small_data'))

        expected = ['Tous',
                    u'Aurelie',
                    'Bernard',
                    'Camille']
        self.assertEqual(get_persons(), expected)

    def test_get_memberships(self):
        self.client.get(reverse('load_small_data'))

        expected = ['Tous',
                    'Aurelie Dutronc - contact du projet Association de Guiseniers',
                    'Bernard Dutronc - contact du projet Association de Paris',
                    "Camille Dutronc - contact du projet Association de Saint-Pierre d'Aurillac"]
        self.assertEqual(get_memberships(),  expected)
