from ports.social_port import *


class SocialAdapter(SocialPort):
    
    def connect_strava(user_id:str, strava_auth_code:str)-> bool:
        ...
        
    def disconnect_strava(user_id:str)-> bool:
        ...
        
    def share_to_sical(user_id:str, url:str, platform:str)-> bool: 
        ...
        

