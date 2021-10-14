import requests
import pprint
from argparse import ArgumentParser

pp = pprint.PrettyPrinter()

parser = ArgumentParser()
parser.add_argument("-a", "--addr", type=str, required=True, help="Stream Address URL")
parser.add_argument("-u", "--user", type=str, required=True, help="API Username")
parser.add_argument("-p", "--pswd", type=str, required=True, help="API pswdword")
parser.add_argument("-i", "--input", type=str, required=True, help="path to json payload")
args = parser.parse_args()

req = requests.get(args.addr + "/api/admin/status", auth=(args.user, args.pswd))

print(req.status_code)
print(req.headers['content-type'])
pp.pprint(req.json())