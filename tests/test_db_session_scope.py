# ruta: tests/test_db_session_scope.py
def test_session_scope_1(db_conn_session):
    assert db_conn_session["status"] == "ok"

def test_session_scope_2(db_conn_session):
    assert db_conn_session["status"] == "ok"
