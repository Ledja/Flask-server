# The general purpose of the server is to create and retrieve people.
# People are manager on resource /people/ and /people/<:id>.
# We also want to make sure that the server is healthy, therefore,
# we have a resource /_ping. This endpoint only supports HTTP HEAD method and
# for other HTTP methods returns 405 status code to let the client know that
# the requested method is not implemented (https://httpstatuses.com/)
# In order to execute the client there is the only requirement
# needed - `requests` .
# You can install by `pip install requests`

import argparse
import json

import requests
from urllib import parse


def run(server_port):
    url = f'http://localhost:{server_port}'

    test_ping_endpoint(url)

    headers = {'accept': 'application/json',
               'content-type': 'application/json'}
    # create person with non integer age fails
    person_response = requests.post(
        parse.urljoin(url, 'person/'),
        data=json.dumps({'name': 'John doe', 'age': '40 years'}),
        headers=headers)
    assert person_response.status_code == 400, \
        f"Create person request with non-integer age should return " \
        f"Bad request but it returned: {person_response.status_code}"
    assert person_response.json() == {'age': ['Not a valid integer']}

    # create person with age > 100 fails
    person_response = requests.post(
        parse.urljoin(url, 'person/'),
        json={'name': 'John doe', 'age': 400}, headers=headers)
    assert person_response.status_code == 400, \
        f"Create person didn't return expected status code, it " \
        f"returned {person_response.status_code}"
    assert person_response.json() == \
           {'age': ['Person too old. Max age is 100']}, \
        f"Create person didn't return expected response, it returned: " \
        f"{person_response.json()}"

    # create person
    person_response = requests.post(
        parse.urljoin(url, 'person/'),
        json={'name': 'John doe', 'age': 40}, headers=headers)
    assert person_response.status_code == 201, \
        f"Create person didn't return expected status code, it returned: " \
        f"{person_response.status_code}"
    assert set(person_response.json()) ^ \
           set({'name': 'John Doe', 'age': 40}.items())

    # get person with ID returned by create operation
    person_id = person_response.json()['id']
    person_response = requests.get(
        parse.urljoin(url, f'person/{person_id}'),
        headers={'accept': 'application/json'})
    assert person_response.status_code == 200, \
        f"Get person didn't return expected status code, " \
        f"it returned: {person_response.status_code}"

    # get person with nonexistent ID fails
    person_id = person_response.json()['id']
    person_response = requests.get(
        parse.urljoin(url, f'person/{person_id + 1}'),
        headers={'accept': 'application/json'})
    assert person_response.status_code == 404

    print("Well done!")


def test_ping_endpoint(base_url):
    get_response = requests.get(parse.urljoin(base_url, '_ping'))
    assert get_response.status_code == 405, \
        "HTTP Method GET should not be allowed on /_ping endpoint"
    head_response = requests.head(parse.urljoin(base_url, '_ping'))
    assert head_response.status_code == 200, \
        f"HTTP Method HEAD should return OK on /_ping endpoint but it " \
        f"returned: {head_response.status_code}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Awesome client')
    parser.add_argument('--port', type=int, default=9876, help='Server port')
    args = parser.parse_args()
    run(args.port)
