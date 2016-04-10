def test_request(client):
    response = client.get('/question/batch/')

    assert response.status_code == 200
    template_names = [i.name for i in response.templates]
    assert 'question/batch.html' in template_names
    assert 'base.html' in template_names
