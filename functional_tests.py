from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import unittest

import time

DEFAULT_WAIT = 20  # seconds


class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):  
        # Elisabeth has heard about a cool new online to-do app. She goes to 
        # check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text  
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Feed the ducks" into a text box 
        inputbox.send_keys('Feed the ducks')  

        # When she hits enter, the page updates, and now the page lists
        # "1: Feed the ducks" as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        table = WebDriverWait(self.browser, DEFAULT_WAIT).until(
            EC.presence_of_element_located((By.ID, 'id_list_table'))
        )
        # table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Feed the ducks', [row.text for row in rows])

        # There is still a text box inviting her to add another item. She enters 
        # "Don't forget to close the fence" (we can't have the ducks wander off 
        # onto the street).
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Don\'t forget to close the fence')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        # The page updates again, and now shows both items on her list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('2: Don\'t forget to close the fence', [row.text for row in rows])
        self.fail('Finish the test!')

        # Elisabeth wonders whether the site will remember her list. Then she 
        # sees that the site has generated a unique URL for her -- there is some 
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes to sleep.

if __name__ == '__main__':  
    unittest.main()  
