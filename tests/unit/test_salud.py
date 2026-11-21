from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "ok"}


def test_inicio(client: TestClient) -> None:
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert "Facturacion Electronica" in respuesta.text
