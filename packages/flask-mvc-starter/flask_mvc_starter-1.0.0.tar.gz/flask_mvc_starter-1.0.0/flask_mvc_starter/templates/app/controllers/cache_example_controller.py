from flask_restful import Resource
from datetime import datetime
from app.extensions import cache


class TimeResource(Resource):
    @cache.cached(timeout=60)
    def get(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {
            'time': current_time,
            'message': 'This time is cached for 10 seconds. Call multiple times to see it stays the same.'
        }, 200


class ClearCacheResource(Resource):
    def post(self):
        cache.clear()
        return {
            'message': 'Cache cleared successfully'
        }, 200
