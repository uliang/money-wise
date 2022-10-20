import pytest 

from django.core import mail 
from django.contrib.auth import get_user_model 

from registration.exceptions import DuplicateUserNameError, UnvalidatedUserError
from registration.service import create_user 



@pytest.mark.django_db
@pytest.mark.usefixtures("register_new_user")
def test_create_new_user_service_creates_new_user_if_not_present(cursor): 
    result = cursor.execute("select username from auth_user ").fetchone() 
    assert result == ('john@example.com', )  

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user")
def test_that_new_user_cannot_be_created_if_already_present(): 
    with pytest.raises(DuplicateUserNameError) as exc: 
        create_user('john@example.com', 'p@s$w0rd')
    
        assert str(exc) == "User john@example.com already registered."

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user")
def test_that_validation_email_is_sent_when_new_user_is_successfully_saved_in_db(): 
    assert len(mail.outbox) == 1    
    message = mail.outbox[0] 

    assert message.subject == "New user validation link" 
    assert message.from_email == "admin@money-wise.com.my"
    assert message.to == ["john@example.com"]

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
def test_that_get_full_name_method_on_user_returns_email(): 
    user = get_user_model().objects.get(username='john@example.com')
    assert user.get_full_name() == "john@example.com" 

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user") 
def test_that_get_short_name_method_on_user_returns_email(): 
    user = get_user_model().objects.get(username='john@example.com')
    assert user.get_short_name() == "john"
