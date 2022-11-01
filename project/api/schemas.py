from ninja import ModelSchema, Schema

from django.contrib.auth import get_user_model

from account_management.models import Account 

from account_management.models import Ledger


class UserSchema(Schema): 
    username: str 
    password: str


class UserResponseSchema(ModelSchema): 
    class Config: 
        model = get_user_model() 
        model_exclude = ['password', 'validation_token']

class LedgerSchema(ModelSchema): 
    class Config: 
        model = Ledger 
        model_fields = ['number', 'name', 'description'] 


class LedgerResponseSchema(ModelSchema): 
    class Config: 
        model = Ledger 
        model_exclude = ['user']
    
class AccountSchema(ModelSchema): 
    class Config:
        model = Account 
        model_fields = ['number', 'name', 'description', 'notes', 'debit_account']

class AccountResponseSchema(ModelSchema): 
    class Config:
        model = Account 
        model_fields = ['id', 'number', 'name', 'description', 'notes', 
                        'debit_account']

