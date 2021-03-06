# myapp/handlers.py
from corsheaders.signals import check_request_enabled


def cors_allow_api_to_everyone(sender, request, **kwargs):
    return 'webhook' in request.path


check_request_enabled.connect(cors_allow_api_to_everyone)
