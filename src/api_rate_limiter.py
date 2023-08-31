"""
This module creates a simple API Rate Limiter, a tool that 
monitor the number of requests per a window of time a service agrees to allow.
"""
from collections import defaultdict, deque
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import json
import logging


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class APIRateLimiter():
    """
    A class for API Rate Limiter

    '''
    Attributes
    ----------
    time_interval : int
        The amount of time to wait before the previous call clears up (default 10000 milliseconds)
    count : int
        Numbers of calls allowed in time interval timeframe
    """

    def __init__(self, time_interval=10000, count=5):
        """ 
        Constructs all the necessary attributes for the APIRateLimiter object.

        '''
        Parameters
        ----------
        time_interval : int
            The amount of time to wait before the previous call clears up 
            (default 10000 milliseconds)
        count : int
            Numbers of calls allowed in time interval timeframe
        client_requests : dict
            Dictionary with 
                key: IP Address 
                value: list of time each visit in the current time inverval
        """
        self.time_interval = time_interval
        self.count = count
        self.client_requests = defaultdict(deque)

    def limit_check(self, ip_address):
        """
        A function that checks to see if the limit has been reached.

        '''
        Parameters
        ----------
        ip_address : str
            IP Address from the client
        """

        self.clean_calls() # Clean up calls that were passed decided window time

        # Append to the list if request count is less than the numbers
        # of calls allowed in the itme interval timeframe
        if len(self.client_requests[ip_address]) < self.count:
            self.client_requests[ip_address].append(time.time()*1000)
            return True
        return False

    def clean_calls(self):
        """
        A function that clean up calls after it passed the decided window time
        """
        # Remove calls from the list that are passed the decided window time
        for _, requests in self.client_requests.items():
            if requests and self.time_interval < (time.time()*1000 - requests[0]):
                requests.popleft()


class RequestHandler(BaseHTTPRequestHandler):
    """ 
        Constructs all the necessary attributes for the RequestHandler object.
        Takes on BaseHTTPRequestHandler which handle the HTTP requests that arrive at the server.
    """

    rate_limiter = APIRateLimiter()

    def response(self, code, message, content_type):
        """
        A function that process response code, message and content type and send to the server
        
        '''
        Parameters
        ----------
        code : int
            HTTP response status code
        message : str
            IP Address from the client
        content_type : str
            message content type, currently support JSON only
        """
        self.send_response(code)
        self.send_header('content-type', content_type)
        self.end_headers()
        self.wfile.write(json.dumps(message).encode())


    def do_GET(self):
        """
        A function that pass information and calls response method
        """
        # get client IP address and it's visit list
        ip_address = self.address_string()
        current_requests = self.rate_limiter.client_requests[ip_address]

        # Check whether the IP address reach limit and send approaite messages and response code
        if self.rate_limiter.limit_check(ip_address):
            current_request_count = len(current_requests)
            message = f'current time is:' \
            f'{time.ctime()}, {ip_address} have {current_request_count} requests in last 10 seconds'
            logging.info(message)
            self.response(200, {'Message': message}, 'application/json')
        else:
            wait_time = round((10000 - (time.time()*1000 - current_requests[0]))/1000)
            message = f"Rate limit exceeded, need wait {wait_time} seconds"
            logging.error(message)
            self.response(429, {'Error': message}, 'application/json')


def main():
    """
    main method calls HTTPServer with specific PORT
    """
    PORT = 8000
    server = HTTPServer(('localhost', PORT), RequestHandler)
    logging.info(f"Server running on port {PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
