import time
from datetime import timedelta
import pytest 

from django.core import mail 
from django.contrib.auth import get_user_model 
from django.test import override_settings

from registration.exceptions import DuplicateUserNameError, UnvalidatedUserError
from registration.service import create_user 



@pytest.mark.django_db
@pytest.mark.usefixtures("register_new_user")
def test_create_new_user_service_creates_new_user_if_not_present(cursor): 
    result = cursor.execute("select username from registration_user ").fetchone() 
    assert result == ('john@example.com', )  

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user")
def test_that_new_user_cannot_be_created_if_already_present(): 
    with pytest.raises(DuplicateUserNameError) as exc: 
        create_user('john@example.com')
    
        assert str(exc) == "User john@example.com already registered."

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user")
def test_that_validation_email_is_sent_when_new_user_is_successfully_saved_in_db(): 
    assert len(mail.outbox) == 1    
    message = mail.outbox[0] 

    assert message.subject == "New user validation link" 
    assert message.from_email == "admin@money-wise.com.my"
    assert message.to == ["john@example.com"]
    assert 'registration/validate?username=john@example.com&token=abc' in message.body 

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user") 
def test_that_email_is_not_sent_when_user_info_is_updated(): 
    mail.outbox = [] 

    User = get_user_model() 
    user = User.objects.get(username="john@example.com")
    user.first_name = 'John'
    user.save()
    
    assert len(mail.outbox) == 0 

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user") 
def test_that_clicked_validation_link_validates_user(client): 
    response =client.get('/registration/validate?username=john@example.com&token=abc')
    user = get_user_model().objects.get(username='john@example.com')
    
    assert user.is_validated == True


@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user") 
def test_that_unvalidated_user_cannot_set_password(): 
    user = get_user_model().objects.get(username='john@example.com')

    with pytest.raises(UnvalidatedUserError) as exc: 
        user.set_password('password') 
        assert str(exc) == "Password cannot be set on unvalidated users."

@pytest.mark.django_db
@pytest.mark.usefixtures("register_new_user") 
@override_settings(
    VALIDATION_TOKEN_EXPIRY = timedelta(seconds=0.5)
)
def test_that_user_cannot_be_validated_if_validation_link_has_expired(client): 
    time.sleep(0.6) 
    response =client.get('/registration/validate?username=john@example.com&token=abc')
    
    user = get_user_model().objects.get(username='john@example.com')
    assert user.is_validated==False
    
@pytest.mark.django_db
@pytest.mark.usefixtures("register_new_user") 
def test_send_message_callback_sends_message_with_urlsafe_token_if_none_supplied(): 
    validation_token = get_user_model().objects.get(username='john@example.com').validation_token 
    body = mail.outbox[0].body 
    assert validation_token in body 

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user") 
def test_that_get_full_name_method_on_user_returns_email(): 
    user = get_user_model().objects.get(username='john@example.com')
    assert user.get_full_name() == "john@example.com" 

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user") 
def test_that_get_short_name_method_on_user_returns_email(): 
    user = get_user_model().objects.get(username='john@example.com')
    assert user.get_short_name() == "john"
