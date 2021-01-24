from instamojo_wrapper import Instamojo
from django.conf import settings

api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN,
                endpoint='https://test.instamojo.com/api/1.1/')
