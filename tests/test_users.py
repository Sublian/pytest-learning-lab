# tests/test_users.py
def test_user_creation(init_db, user_data):
    """Comprueba que el usuario se crea correctamente y se guarda en la DB."""
    assert init_db["connected"] is True
    assert user_data in init_db["users"]
    print(f"✅ Usuario {user_data['name']} activo en DB")


def test_user_is_unique(init_db, user_data):
    """Cada test debe tener un usuario diferente."""
    all_ids = [u["id"] for u in init_db["users"]]
    assert len(set(all_ids)) == len(all_ids)
    print(f"🔄 Base de datos contiene {len(all_ids)} usuarios únicos")
