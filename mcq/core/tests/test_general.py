def test_home(client):
    response = client.get('/')
    #import pdb;pdb.set_trace()

    assert response.status_code == 200
    assert response.template_name == ['home.html']
