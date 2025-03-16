from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status
from ..models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'Ulug'
    assert response.json()['email'] == 'ulug@gmail.com'
    assert response.json()['first_name'] == 'Ulugbek'
    assert response.json()['last_name'] == 'Urakov'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '998974795636'

# def test_change_password_success(test_user):
#     response = client.put('/user/password', json={'password': 'test1234', 'new_password': 'test12345'})
#     assert response.status_code == status.HTTP_204_NO_CONTENT

# def test_change_password_invalid_current_password(test_user):
#     response = client.put('/user/password', json={'password': 'wrong_password', 'new_password': 'test1234578'})
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json() == {'detail': 'Error on password change'}

# def test_change_phone_number_success(test_user):
#     response = client.put('/user/phonenumber/998974795636')
#     assert response.status_code == status.HTTP_204_NO_CONTENT