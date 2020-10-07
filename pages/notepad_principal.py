class NotepadPrincipal:

    NEW_ARQ = {
        "control_type": "ControlType.Document",
        "class_name": "Edit"
    }

    def __init__(self, application):
        self.app = application

    def click_new_arq(self, text):
        self.app.find_element(self.NEW_ARQ).send_keys(text)
