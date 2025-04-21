'''
Users/Middleware/Log_requests.py - It contains logging information for 
all requests made to the server each day
'''
import logging
from datetime import date, datetime

class RequestLoggingMiddleware():
    ''' Middleware class to log requests day-wise'''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        '''
            Middleware to log Requests along with their response.
        '''
        # Configurations for the Logger.
        today = date.today()
        logger = logging.getLogger("Request_logger")
        logging.basicConfig(filename=f"./LOGS/{today}.log", encoding="utf-8", level=logging.DEBUG)

        # Parameters to be logged - Before Response
        access_time = datetime.now().time()
        method = request.method
        path = request.META['PATH_INFO']
        if method in ['PUT', 'POST']:
            request_data = request.body
        else:
            request_data = 'No Data Recieved!'

        # Get Response
        response = self.get_response(request)

        # Parameters to be logged - After Response
        user = request.user
        if user.is_authenticated:
            role = user.role
        else:
            role = 'Guest'
        status_code = response.status_code
        try:
            response_data = response.data
        except Exception:
            response_data = 'JSON Data not sent'

        # Logging the data in the file.
        logger.log(
            level=logging.INFO,
            msg=f'''\n\tACCESS_TIME = {access_time};
            USER = "{user}";
            ROLE = "{role}";
            METHOD = "{method}";
            PATH = "{path}";
            REQUEST_DATA = {request_data};
            STATUS_CODE = "{status_code}";
            RESPONSE_DATA = {response_data}\n''')
        return response
