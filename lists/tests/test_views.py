from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List
from superlists import settings as superlists_settings


class HomePageTest(TestCase):
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
        

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        item_text = 'A new list item'
        self.client.post('/lists/new', data={'item_text': item_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')
    
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        itemeys = ['itemey 1', 'itemey 2']
        for txt in itemeys:
            Item.objects.create(text=txt, list=correct_list)
        
        other_list = List.objects.create()
        other_itemeys = ['other itemey 1', 'other itemey 2']
        for txt in other_itemeys:
            Item.objects.create(text=txt, list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')
        
        for txt in itemeys:
            self.assertContains(response, txt)
        for txt in other_itemeys:
            self.assertNotContains(response, txt)

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

class UtilsTest(TestCase):
    """Test any util functions"""
    
    def test_strtobool(self):
        for s in ['TRUE', 'True', 'true', 'TrUe', '1', 't', 'T']:
            self.assertTrue(superlists_settings.strtobool(s))
        # anything else should return false
        for s in ['False', '0', 'bla']:
            self.assertFalse(superlists_settings.strtobool(s))
