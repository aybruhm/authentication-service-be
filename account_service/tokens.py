# Djang Imports
from django.contrib.auth.tokens import PasswordResetTokenGenerator  
from django.utils import six


class EmailActivationTokenGenerator(PasswordResetTokenGenerator):  
    
        def _make_hash_value(self, user, timestamp):  
            return (  
                six.text_type(user.pk) + six.text_type(timestamp) +  
                six.text_type(user.is_active)  
            )
            
email_activation_token = EmailActivationTokenGenerator()