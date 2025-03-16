'''
This file contains the tests for the views.py file.
'''

def test_create_cocktail(test_client, mock_openai_client):
    '''
    Test the create_cocktail endpoint with a mocked OpenAI response.
    '''

    with mock_openai_client("Mocked cocktail Response"):
        response = test_client.get('/create_cocktail', json = {'input': "chicken, rice, broccoli"})

    assert response.status_code == 200
    data = response.get_json()
    assert 'cocktail' in data
    assert isinstance(data['cocktail'], str)
    assert len(data['cocktail']) > 0


def test_index(test_client):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check the response is valid and contains the expected text
    '''
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Cocktail Generator' in response.data

def test_create_cocktail_no_ingredients(test_client):
    '''
    Test the create_cocktail endpoint with no ingredients.
    '''

    response = test_client.post('/create_cocktail', json={})  # Missing 'input' key
    assert response.status_code == 400
    assert response.get_json()['error'] == "No ingredients provided"

    response = test_client.post('/create_cocktail', json={'input': ''})  # Empty string
    assert response.status_code == 400
    assert response.get_json()['error'] == "No ingredients provided"

    response = test_client.post('/create_cocktail', json={'input': '  '})  # Whitespace only
    assert response.status_code == 400
    assert response.get_json()['error'] == "No ingredients provided"
