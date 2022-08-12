# Third Party Imports
import httpx

# Django Imports
from django.conf import settings
from django.core.exceptions import ValidationError

# Google ID Token
GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'


async def google_validate_id_token(*, id_token: str) -> bool:
    """
    Authenticate this request by comparing the aud (short for audience) 
    from the Google response with the GOOGLE_OAUTH2_CLIENT_ID
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GOOGLE_ID_TOKEN_INFO_URL,
            params={'id_token': id_token}
        )

        # Check is response is not "OK"
        if not response.ok:
            raise ValidationError('id_token is invalid.')

        # Get audience data
        audience = response.json()['aud']

        # Compare audience with that of the settings 
        # configured oauth2 google client id
        if audience != settings.GOOGLE_OAUTH2_CLIENT_ID:
            raise ValidationError('Invalid audience.')

        return True