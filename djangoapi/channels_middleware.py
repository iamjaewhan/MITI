from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from jwt import decode as jwt_decode



@database_sync_to_async
def get_user(token):
    """_summary_
    토큰의 소유 유저 객체 반환

    Args:
        token : access token

    Returns:
        User: 유저
    """
    try:
        token_data = UntypedToken(token)
        return get_user_model().objects.get(id=token_data['user_id'])
    except (InvalidToken, TokenError, get_user_model().DoesNotExist, InvalidToken, TokenError):
        raise AuthenticationFailed()

class JwtAuthMiddleware(BaseMiddleware):
    """_summary_
    header의 authorization key의 토큰을 사용하여 사용자를 확인하는 middleware
    """
    
    def __init__(self, inner):
        self.inner = inner
 
    async def __call__(self, scope, receive, send):
        close_old_connections()

        token = scope['headers'][4][1].decode('utf8').split()[1]
        headers = dict(scope['headers'])
        
        try:
            token_name, token = headers[b'authorization'].decode('utf8').split()
        except (IndexError, KeyError) as e:
            raise NotAuthenticated()
            
        scope['user'] = await get_user(token)
        return await super().__call__(scope, receive, send)
    
    def JwtAuthMiddlewareStack(inner):
        return JwtAuthMiddleware(AuthMiddlewareStack(inner))
