# requests is used to send http api requests
from requests import post
# json is used to load payload from .json files
from json import load, dumps
# os.path is used to check if input file exists
from os.path import exists
# sys is used to end the program
from sys import exit
# argparse is used to gather user input
from argparse import ArgumentParser
# pprint is used to pretty print the api response
from pprint import PrettyPrinter


def main():

    # parse user input
    arguments = parse_arguments()

    # open and read the JSON file
    payload = load_json(arguments.input)

    # send the API requests
    responses = send_api_requests(payload, arguments)

    # print the API response
    print_response(responses)


# parse user input
def parse_arguments():
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        "-a", "--addr", type=str, required=True, help="Stream Address URL")
    argument_parser.add_argument(
        "-u", "--user", type=str, required=True, help="API Username")
    argument_parser.add_argument(
        "-p", "--pswd", type=str, required=True, help="API pswdword")
    argument_parser.add_argument(
        "-i", "--input", type=lambda x: is_valid_file(argument_parser, x), required=True, help="path to json payload")
    argument_parser.add_argument(
        "-l", "--latency", type=int, required=False, default=-1, choices=range(5), help="Optional Latency")

    return argument_parser.parse_args()


# open and read the JSON file
def load_json(path):
    with open(path) as json_file:
        payload = load(json_file)
        json_file.close()
    return payload

# send the API requests
def send_api_requests(payload, arguments):
    responses = []
    responses.append(post(arguments.addr + "/api/admin/config/video/streamoutputvariants", json=payload, auth=(arguments.user, arguments.pswd)))
    
    if (arguments.latency >= 0):
        latency_data = { "value": arguments.latency }
        responses.append(post(arguments.addr + "/api/admin/config/video/streamlatencylevel", data=dumps(latency_data), auth=(arguments.user, arguments.pswd)))

    return responses

# display the API response
def print_response(responses):
    # create the pretty printer
    pretty_printer = PrettyPrinter()

    # print responses
    for i, response in enumerate(responses):
        print("Request " + str(i+1) + ":")
        print(response.status_code)
        print(response.headers['content-type'])
        pretty_printer.pprint(response.json())
        print()


# check if the input file exists
def is_valid_file(parser, path):
    if not exists(path):
        parser.error("The file %s does not exist!" % path)
    else:
        return path


# main hook
if __name__ == '__main__':
    exit(main())
