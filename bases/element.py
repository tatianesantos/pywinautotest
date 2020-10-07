"""Element module."""


class Element:
    """A wrapper class for pywinauto element class."""

    def __init__(self, element, logger):
        self.logger = logger
        self.element = element
        self.selectors = self.element.criteria[1:]

    def click(self,):
        """Click the specified element."""
        self.logger.info(f"Click on element: {self.selectors}")
        self.element.click_input()

    def send_keys(self, keys):
        """Send keys to the element.

        Parameters
        ----------
        keys : str
            Keys to send, can contain special characters (see Keys class)
        """
        self.logger.info(f"Send '{keys}' to element: {self.selectors}")
        self.element.set_text(keys)

    def set_focus(self):
        """Set focus to an element."""
        self.logger.info(f"Set focus on element: {self.selectors}")
        self.element.set_focus()
