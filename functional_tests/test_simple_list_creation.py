from .base import TodoFunctionalTest
from selenium import webdriver

class NewVisitorTest(TodoFunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):

        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box
        # (Edith's hobby is tying fly-fishing lures)
        self.enter_a_new_item('Buy peacock feathers')

        # When she hits enter, she is taken to a new URL,
        #and now the page lists "1. Buy peacock feathers"
        #as an item in a to-do lists.
        edith_list_url = self.browser.current_url
        self.assertRegexpMatches(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1. Buy peacock feathers')
        #import time
        #time.sleep(15)

        # There is still a text box inviting her to add another item.
        # She enters 'Use peacock feathers to make fly'
        # (Edith is very methodolical)
        self.enter_a_new_item('Use peacock feathers to make fly')

        # The homepage updates again, and now shows both items on her lists.
        self.check_for_row_in_list_table('1. Buy peacock feathers')
        self.check_for_row_in_list_table('2. Use peacock feathers to make fly')

        #Now a new user, Francis, comes along.

        #We use a new browser session to make sure no information
        #of Edith's comes along (EG cookies, localStorage)
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Francis visits the home page. There is no sign of Edith's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make fly', page_text)

        #Francis starts a new list by entering a new item
        #He is less interesting than Edith
        self.enter_a_new_item('Buy milk')

        #Francis gets his own url
        francis_list_url = self.browser.current_url
        self.assertRegexpMatches(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #There is still no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, she goes back to sleep.

    def test_can_delete_an_existing_item(self):
        # Edith goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She enter a new item
        self.enter_a_new_item('Buy peacock feathers')

        # The homepage updates and now shows this first item
        self.check_for_row_in_list_table('1. Buy peacock feathers')

        # She goes to buy peacock feathers, so now she deletes the item
        delete_link = self.browser.find_element_by_tag_name('a')
        delete_link.click();

        # Now the list no longer shows the item she has just deleted
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)

    def test_layout_and_styling(self):
        # She goes to check out its homepage.
        self.browser.set_window_size(1024, 768)
        self.browser.get(self.live_server_url)

        # She notices that the input box is nicely centered
        self.check_input_box_is_centered()

        # She starts a new list
        self.enter_a_new_item('testing')
        self.check_input_box_is_centered()

    def check_input_box_is_centered(self):
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width']/2),
            512,
            delta=5
        )
