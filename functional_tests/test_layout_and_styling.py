from .base import TodoFunctionalTest

class LayoutAndStylingTest(TodoFunctionalTest):
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
