# tests/test_hello.py
def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == 'Congratulation! Server still works!'
