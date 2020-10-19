"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

import traceback


def index():
    index_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <h1>My WSGI Calculator</h1><h4>by David Burnett</h4>
        <!-- Codes by HTML.am -->
        <p>Use this calculator to add, subtract, multiply, or divide two numbers.</p>
        <br>
        <p>http://localhost:8080</p>
        <br>
        <p>Add function and numbers to the URL as show below.  See table below 
        for example of operations</p>
        <!-- CSS Code -->
        <style type="text/css" scoped>
        table.GeneratedTable {
        width:50%;
        background-color:#FFFFFF;
        border-collapse:collapse;border-width:1px;
        border-color:#336600;
        border-style:solid;
        color:#009900;
        }

        table.GeneratedTable td, table.GeneratedTable th {
        border-width:1px;
        border-color:#336600;
        border-style:solid;
        padding:2px;
        }

        table.GeneratedTable thead {
        background-color:#CCFF99;
        }
        </style>

        <!-- HTML Code -->
        <table class="GeneratedTable">
        <thead>
        <tr>
        <th>Function</th>
        <th>Address</th>
        <th>Operation</th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <td>Add</td>
        <td>http://localhost:8080/add/num1/num2 </td>
        <td>num1 + num2</td>
        </tr>
        <tr>
        <td>Subtract</td>
        <td>http://localhost:8080/subtract/num1/num2</td>
        <td>num1 - num2</td>
        </tr>
        <tr>
        <td>Multiply</td>
        <td>http://localhost:8080/multiply/num1/num2</td>
        <td>num1 * num2</td>
        </tr>
        <tr>
        <td>Divide</td>
        <td>http://localhost:8080/divide/num1/num2</td>
        <td>num1 / num2</td>
        </tr>
        </tbody>
        </table>
    </head>
    <body>

    </body>
    </html>
    """
    return index_page


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    # sum = "0"
    return str(int(args[0]) + int(args[1]))

# TODO: Add functions for handling more arithmetic operations.


def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    return str(int(args[0]) * int(args[1]))


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    return str(int(args[0]) - int(args[1]))


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    return str(int(args[0]) / int(args[1]))


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    # func = add
    # args = ['25', '32']
    funcs = {
        '': index,
        'add': add,
        'subtract': subtract,
        'divide': divide,
        'multiply': multiply,
    }

    path = path.strip('/').split('/')
    func_name = path[0]
    args = (path[1:])

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    return func, args


def application(environ, start_response):
    """
    application function to take environ and start_response variables

    environ points to a dictionary containing CGI like environment variables
    which is populated by the server for each received request from the client

    start_response is a callback function supplied by the server which takes
    the HTTP status and headers as arguments

    Returns the response body, wrapped in a list although it could be any
    iterable.
    """
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Dividing by zero</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server

    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
