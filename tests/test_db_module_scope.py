# ruta: tests/test_db_module_scope.py
def test_mod_scope_1(db_conn_module):
    assert db_conn_module["status"] == "ok"

def test_mod_scope_2(db_conn_module):
    assert db_conn_module["status"] == "ok"
