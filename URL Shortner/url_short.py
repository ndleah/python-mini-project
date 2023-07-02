# necessary imports
from __future__ import with_statement
import contextlib
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from urllib.request import urlopen


# function to create tiny url with an api request


def create_tiny_url(url):
    request_url = ('http://tinyurl.com/api-create.php?' +
                   urlencode({'url': url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')


inp = input("Enter or paste the lengthy url of the domain: ")

# the result is printed by calling the defined function
result = create_tiny_url(inp)
print("The Short URL is: ", result)
