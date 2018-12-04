from .base import FunctionalTest
from selenium import webdriver


class NewVisitorTest(FunctionalTest):
    
    def test_one_user_can_start_a_list_and_retrieve_it_later(self):  
        # E has heard about a cool new online to-do app. She goes to 
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

        # E wonders whether the site will remember her list. Then she 
        # sees that the site has generated a unique URL for her -- there is some 
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # E starts a new to-do list
        self.browser.get(self.live_server_url)
        self.input_todo_item('Feed the ducks')
        self.wait_for_row_in_list_table('1: Feed the ducks')

        # She notices that her list has a unique URL
        E_list_url = self.browser.current_url
        self.assertRegex(E_list_url, '/lists/.+')
        
        # Now a new user, J, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of E's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # J visits the home page. There is no sign of E's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        for txt in ['Feed the ducks', 'close the fence']:
            self.assertNotIn(txt, page_text)

        # J starts a new list by entering a new item.
        self.input_todo_item('Buy E 20kg waterfowl pellets')
        self.wait_for_row_in_list_table('1: Buy E 20kg waterfowl pellets')

        # J gets his own unique URL
        J_list_url = self.browser.current_url
        self.assertRegex(J_list_url, '/lists/.+')
        self.assertNotEqual(J_list_url, E_list_url)

        # Again, there is no trace of E's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Feed the ducks', page_text)
        self.assertIn('Buy E 20kg', page_text)

        # Satisfied, they both go back to sleep
