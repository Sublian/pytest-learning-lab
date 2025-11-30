from src.workflow.notificador import Notificador

def test_spy_llamadas_basicas(mocker):
    n = Notificador()

    spy_validar = mocker.spy(n, "validar_mensaje")
    spy_enviar = mocker.spy(n, "enviar_mensaje")

    r = n.procesar("hola")

    assert r["ok"] is True
    assert spy_validar.call_count == 1
    assert spy_enviar.call_count == 1

def test_spy_argumentos(mocker):
    n = Notificador()

    spy_validar = mocker.spy(n, "validar_mensaje")

    n.procesar("  hola  ")

    # Obtenemos los args (tupla) y kwargs (dict)
    args, kwargs = spy_validar.call_args

    assert args[0].strip() == "hola"
    assert kwargs == {}

def test_spy_orden(mocker):
    n = Notificador()

    spy_validar = mocker.spy(n, "validar_mensaje")
    spy_enviar = mocker.spy(n, "enviar_mensaje")

    n.procesar("xyz")

    # Verificando orden (llamadas intercaladas)
    lista = [spy_validar.call_args_list, spy_enviar.call_args_list]

    assert len(lista[0]) == 1   # validar fue llamado primero
    assert len(lista[1]) == 1   # luego enviar

def test_spy_caso_invalido(mocker):
    n = Notificador()
    
    spy_validar = mocker.spy(n, "validar_mensaje")
    spy_enviar = mocker.spy(n, "enviar_mensaje")

    r = n.procesar("  ")  # mensaje vacío

    assert r["ok"] is False
    assert spy_validar.call_count == 1
    assert spy_enviar.call_count == 0
