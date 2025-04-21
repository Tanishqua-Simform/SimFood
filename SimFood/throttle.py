'''
SimFood/Throttle.py - It contains Throttle Classes for -
1. Users are scoped based on Request methods - GET, PUT, POST
2. Payment (PUT) for making payment request only thrice a day.
'''
from rest_framework.throttling import UserRateThrottle

class CustomGetThrottleClass(UserRateThrottle):
    ''' User with scope of GET requests '''
    scope = 'user-get'
    def allow_request(self, request, view):
        if request.method != 'GET':
            return True
        return super().allow_request(request, view)

class CustomPostThrottleClass(UserRateThrottle):
    ''' User with scope of POST requests '''
    scope = 'user-post'
    def allow_request(self, request, view):
        if request.method != 'POST':
            return True
        return super().allow_request(request, view)

class CustomPutThrottleClass(UserRateThrottle):
    ''' User with scope of PUT requests '''
    scope = 'user-put'
    def allow_request(self, request, view):
        if request.method != 'PUT':
            return True
        return super().allow_request(request, view)

class CustomPaymentPutThrottleClass(UserRateThrottle):
    ''' User with scope of PUT requests in Payment Process '''
    scope = 'payment-put'
    def allow_request(self, request, view):
        if request.method != 'PUT':
            return True
        return super().allow_request(request, view)
