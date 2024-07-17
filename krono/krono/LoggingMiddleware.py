from django.utils.deprecation import MiddlewareMixin

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger = logging.getLogger('django.request')
        logger.debug(f'Request: {request.method} {request.get_full_path()} from {request.META["REMOTE_ADDR"]}')

    def process_response(self, request, response):
        return response

