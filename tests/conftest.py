from fixture.conftest_fixtures import *
from pages.notepad_principal import NotepadPrincipal



@pytest.fixture(scope="function")
def notepad_principal(app_instance):
    return NotepadPrincipal(app_instance)
