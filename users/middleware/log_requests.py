import logging
from datetime import date, datetime

class RequestLoggingMiddleware():
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
        ACCESS_TIME = datetime.now().time()
        METHOD = request.method
        PATH = request.META['PATH_INFO']
        if METHOD in ['PUT', 'POST']:
            REQUEST_DATA = request.body
        else:
            REQUEST_DATA = 'No Data Recieved!'

        # Get Response 
        response = self.get_response(request)

        # Parameters to be logged - After Response
        USER = request.user
        try:
            ROLE = USER.role
        except Exception:
            ROLE = 'Guest'
        STATUS_CODE = response.status_code
        try:
            RESPONSE_DATA = response.data
        except Exception:
            RESPONSE_DATA = 'JSON Data not sent'

        # Logging the data in the file.
        logger.log(level=logging.INFO, msg=f'\n\tACCESS_TIME = {ACCESS_TIME}; \n\tUSER = "{USER}"; \n\tROLE = "{ROLE}"; \n\tMETHOD = "{METHOD}"; \n\tPATH = "{PATH}"; \n\tREQUEST_DATA = {REQUEST_DATA}; \n\tSTATUS_CODE = "{STATUS_CODE}"; \n\tRESPONSE_DATA = {RESPONSE_DATA}\n')
        return response