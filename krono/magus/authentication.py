"""
Custom authentication classes for MAGUS API
"""
from rest_framework import authentication, exceptions
from django.utils import timezone
from magus.models import APIKey


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication using API keys.
    
    Clients should authenticate by passing the API key in the Authorization header:
        Authorization: Api-Key <api_key>
    """
    keyword = 'Api-Key'
    
    def authenticate(self, request):
        """
        Authenticate the request using an API key.
        
        Returns:
            (user, None) if authentication succeeds
            None if this authentication method is not being used
        
        Raises:
            AuthenticationFailed if authentication fails
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith(self.keyword):
            # This request is not using API key auth, try other methods
            return None
        
        try:
            # Extract key from header: "Api-Key <key>"
            key = auth_header.split(' ')[1]
        except IndexError:
            raise exceptions.AuthenticationFailed('Invalid API key header format')
        
        # Hash the provided key
        key_hash = APIKey.hash_key(key)
        
        # Look up the API key
        try:
            api_key = APIKey.objects.select_related('user').get(
                key_hash=key_hash,
                is_active=True
            )
        except APIKey.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid or inactive API key')
        
        # Update last_used timestamp
        api_key.last_used = timezone.now()
        api_key.save(update_fields=['last_used'])
        
        # Return user associated with this API key
        # DRF expects (user, auth) tuple
        return (api_key.user, api_key)
    
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the WWW-Authenticate
        header in a 401 Unauthenticated response.
        """
        return self.keyword

