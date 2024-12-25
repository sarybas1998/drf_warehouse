import logging
import time

logger = logging.getLogger('api_requests')

class APILoggingMiddleware:
    """
    Middleware для логирования всех входящих запросов к API.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Исключаем некоторые пути из логирования, если необходимо
        # EXCLUDE_PATHS = ['/admin/', '/static/', '/media/']
        # if any(request.path.startswith(path) for path in EXCLUDE_PATHS):
        #     return self.get_response(request)

        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        # Логирование запроса
        method = request.method
        path = request.get_full_path()
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        ip = request.META.get('REMOTE_ADDR')

        logger.info(
            '',
            extra={
                'user': user,
                'ip': ip,
                'method': method,
                'path': path,
                'status': response.status_code,
                'duration': round(duration, 3),
            }
        )

        return response