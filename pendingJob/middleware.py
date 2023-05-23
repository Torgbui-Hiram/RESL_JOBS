from django.conf import settings
from django.contrib.auth import logout
import time


class SessionIdleTimeout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            current_time = int(time.time())
            if last_activity and (current_time - last_activity > settings.SESSION_COOKIE_AGE):
                logout(request)
                del request.session['last_activity']
            else:
                request.session['last_activity'] = current_time
        response = self.get_response(request)
        return response

