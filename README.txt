API Rate Limiter
================ 

Languages choices: Python, Javascript, Golang

Problem statement: In the language of your choice, design a class that can be used as an API rate limiter. 
A rate limiter is a tool that monitors the number of requests per a window of time a service agrees to allow. 
If the request count exceeds the number agreed by the service owner in a decided window time, the rate limiter will reject subsequent calls. 
The rate limiter should limit requests per client by IP address.

Acceptance criteria: 
    -Build a class that can be used by an API to rate limit incoming requests.
    -It should have a function, constructor, or factory method to instantiate an instance that takes an interval in milliseconds and a count that specifies the numbers of calls allowed.
    -A function that checks to see if the limit has been reached.
    -The rate limiter should limit requests per unique IP address and support any number of clients.
    -Build a simple http server (or use a framework) that serves up a GET request that returns the current time in a JSON response and uses the rate limiter you created above, 
    if the rate limit is exceeded return the proper HTTP response code. This can be as simple as using a language's builtin http server.