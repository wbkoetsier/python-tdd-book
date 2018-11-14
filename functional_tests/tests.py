from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
from django.test import LiveServerTestCase

import time

MAX_WAIT = 10  # seconds


class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()
    
    def input_todo_item(self, item_text: str=''):
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)
        
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:  
            try:
                table = self.browser.find_element_by_id('id_list_table')  
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return  
            except (AssertionError, WebDriverException) as e:  
                if time.time() - start_time > MAX_WAIT:  
                    raise e  
                time.sleep(0.5) 

    def test_one_user_can_start_a_list_and_retrieve_it_later(self):  
        # Elisabeth has heard about a cool new online to-do app. She goes to 
        # check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text  
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        # She types "Feed the ducks" into a text box 
        # When she hits enter, the page updates, and now the page lists
        # "1: Feed the ducks" as an item in a to-do list.
        self.input_todo_item('Feed the ducks')
        self.wait_for_row_in_list_table('1: Feed the ducks')

        # There is still a text box inviting her to add another item. She enters 
        # "Don't forget to close the fence" (we can't have the ducks wander off 
        # onto the street).
        # The page updates again, and now shows both items on her list.
        self.input_todo_item('Don\'t forget to close the fence')
        self.wait_for_row_in_list_table('2: Don\'t forget to close the fence')
        
        self.fail('Finish the test!')

        # Elisabeth wonders whether the site will remember her list. Then she 
        # sees that the site has generated a unique URL for her -- there is some 
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Elisabeth starts a new to-do list
        self.browser.get(self.live_server_url)
        self.input_todo_item('Feed the ducks')
        self.wait_for_row_in_list_table('1: Feed the ducks')

        # She notices that her list has a unique URL
        elisabeth_list_url = self.browser.current_url
        self.assertRegex(elisabeth_list_url, '/lists/.+')
        
        # Now a new user, Jasper, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Elisabeth's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Jasper visits the home page. There is no sign of Elisabeth's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        for txt in ['Feed the ducks', 'close the fence']:
            self.assertNotIn(txt, page_text)

        # Jasper starts a new list by entering a new item.
        self.input_todo_item('Buy Elisabeth 20kg waterfowl pellets')
        self.wait_for_row_in_list_table('1: Buy Elisabeth 20kg waterfowl pellets')

        # Jasper gets his own unique URL
        jasper_list_url = self.browser.current_url
        self.assertRegex(jasper_list_url, '/lists/.+')
        self.assertNotEqual(jasper_list_url, elisabeth_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Feed the ducks', page_text)
        self.assertIn('Buy Elisabeth 20kg', page_text)

        # Satisfied, they both go back to sleep

if __name__ == '__main__':  
    unittest.main()  
