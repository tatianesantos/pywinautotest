"""Application Module."""
from bases.element import Element as element_wrapper
from utils.utils import Utils


class Application:
    """Application Module.

    Contains methods and helper objects for interfacing with windows GUI
    application. It models user interactions and one instance of this class
    roughly represents one running the application process in the system.
    """

    def __init__(self, **kwargs):
        self.app = None
        self.pid = None
        self.handle = None
        self.kwargs = kwargs
        self.main_window = None
        self.logger = kwargs.get("logger")
        self.utils = Utils(logger=self.logger)
        jsonpath = "C:/Users/Tatiane/PycharmProjects/templateautomationpywinauto/settings.json"
        self.settings = self.utils.load_json(jsonpath)
        self.executable_path = self.settings["executable_path"]
        self.process_name = self.settings["process_name"]

    def setup(self):
        """Perform setup for the Application class."""
        if self.kwargs.get("auto_start"):
            self.start()

    def teardown(self):
        """Perform teardown for the Application class."""
        if self.kwargs.get("auto_close"):
            self.close()

    def start(self):
        """Start the application.pid

        Cache all the information necessary to easily link this instance
        to a running the application process.
        """
        #self.utils.kill_processes_by_name_filter(self.process_name)
        self.app = self.utils.start_application(self.executable_path)
        self.main_window = self.app.top_window()
        self.pid = self.app.process
        self.main_window.maximize()

    def close(self):
        """Close the application."""
        self.utils.kill_processes_by_name_filter(self.process_name)

    def find_element(self, selectors, parent=None, timeout=10):
        """Find an element satisfies the selectors and is under parent.

        Parameters
        ----------
        parent : int
            Handle of a windows element to search under, may be the top level
            main application window (app.window().handle)
        selectors: dict
            Dict that contains the selectors for the element to search for
        timeout: float, optional
            Seconds to wait for element.exists() before giving up

        Returns
        -------
        obj
            Pywinauto windows element object that satisfies the criteria, None
            if no elements exist that satisfy the criteria

        Notes
        -----
            + Pywinauto returns a wrapper object when you call child_window, so
            this method calls exists() to force it to check and resolve the
            element
            + This method can also be used as a basic wait for exists() for
            specified timeout (10 sec default)
            + To wait for any other conditions and control all aspects of
            wait one should rather use find_element_wrapper method instead
            + We are not sure why, but sometimes the first time you ask for
            exists it can't actually access the element yet, so try a few times
            before giving up
            + This method does not raise a ElementNotFound or similar error,
            because pywinauto doesn't raise that element on child_window or
            exists; _resolve_element will raise a ValueError if the element is
            None a little higher in the call stack
            + child_window does raise an exception if more than one element
            exists that satisfy the criteria

        """
        selectors.update(
            {
                "top_level_only": False,
                "visible_only": True,
                "backend": "uia",
                "found_index": 0,
            }
        )

        if parent:
            parent = self.main_window.child_window(**parent)
        else:
            parent = self.main_window
        self.logger.debug(f"Find element with given selectors: {selectors}")
        element = parent.child_window(**selectors)

        # Retries for {timeout} seconds and retry interval 0.01
        return (
            element_wrapper(element, self.logger)
            if element.exists(timeout, 0.01)
            else None
        )
