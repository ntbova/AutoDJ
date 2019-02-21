from autodj import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
# 
# def test_login(client):
#     response = client.get('/login')
#     assert response


# def test_hello(client):
#     response = client.get('/hello')
#     assert response.data == b'Hello, World!'
