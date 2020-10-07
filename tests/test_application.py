from time import sleep


def test_application(app, notepad_principal):
    sleep(5)
    # Parameters
    __note_text = app.utils.random_string()
    notepad_principal.click_new_arq(__note_text)
