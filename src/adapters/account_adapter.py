from ports.account_port import *


class AcountAdapter(AccountPort):
    def create_account(self, email:str, pwd:str, name:str)->AccountResponse:  
        ...
        
    def get_account(self, token:str)->AccountResponse : 
        ...
        
    def login_account(self, email:str, pwd:str)->AccountResponse : 
        ...
        
    def update_account(self, token:str, acct_response:str)->AccountResponse : 
        ...
        
    def oauth_google(self, email:str, pwd:str)->AccountResponse : 
        ...
        
    def deactivate_account(self, email:str)->bool : 
        ...
        