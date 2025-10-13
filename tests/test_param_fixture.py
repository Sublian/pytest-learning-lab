# tests/test_param_fixture.py
import pytest
from mailing.mail import validar_email

@pytest.fixture(params=[
    ("ok@dom.com", True),
    ("no_at_symbol.com", False),
    ("", False),
])
def email_case(request):
    # request.param contiene la tupla actual
    return request.param

def test_email_cases(email_case):
    email, esperado = email_case
    if esperado:
        assert validar_email(email) is True
    else:
        with pytest.raises(ValueError):
            validar_email(email)
