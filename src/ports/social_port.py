from abc import ABC, abstractmethod


class SocialPort(ABC):
    
    @abstractmethod
    def connect_strava(user_id:str, strava_auth_code:str)-> bool:
        ...
        
    @abstractmethod
    def disconnect_strava(user_id:str)-> bool:
        ...
        
    @abstractmethod
    def share_to_sical(user_id:str, url:str, platform:str)-> bool: 
        ...
        

