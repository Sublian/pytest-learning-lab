# ruta: tests/test_db_function_scope.py
def test_func_scope_1(db_conn_function):
    assert db_conn_function["status"] == "ok"

def test_func_scope_2(db_conn_function):
    assert db_conn_function["status"] == "ok"
