from rest_framework.throttling import UserRateThrottle

class CustomGetThrottleClass(UserRateThrottle):
    scope = 'user-get'
    def allow_request(self, request, view):
        if request.method != 'GET':
            return True
        return super().allow_request(request, view)

class CustomPostThrottleClass(UserRateThrottle):
    scope = 'user-put'
    def allow_request(self, request, view):
        if request.method != 'POST':
            return True
        return super().allow_request(request, view)
    
class CustomPutThrottleClass(UserRateThrottle):
    scope = 'user-put'
    def allow_request(self, request, view):
        if request.method != 'PUT':
            return True
        return super().allow_request(request, view)

class CustomPaymentPutThrottleClass(UserRateThrottle):
    scope = 'payment-put'
    def allow_request(self, request, view):
        if request.method != 'PUT':
            return True
        return super().allow_request(request, view)