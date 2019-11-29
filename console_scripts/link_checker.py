__author__ = 'kuzmenko-pavel'
from os import path
import sys
import json
import requests


session = requests.Session()
session.headers.update({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"})


def checker(from_file, to_file):
    result = []
    from_json_path = path.abspath(from_file)
    with open(from_json_path) as json_file:
        try:
            data = json.load(json_file)
            for item in data:
                partner = item.get('partner')
                r = session.get(partner)
                if r.status_code != requests.codes.ok:
                    continue

                s_click_found = False
                if r.history:
                    for n, h in enumerate(r.history):
                        if 's.click' in h.url:
                            result.append({
                                "id": item.get('id'),
                                "partner": item.get('partner'),
                                "original": h.url
                            })
                            s_click_found = True
                            break
                    if not s_click_found:
                        result.append({
                            "id": item.get('id'),
                            "partner": item.get('partner'),
                            "original": r.history[-1].url
                        })
        except Exception as e:
            print(e)

    to_json_path = path.abspath(to_file)
    with open(to_json_path, "w") as write_file:
        try:
            json.dump(result, write_file, indent=4, sort_keys=True)
        except Exception as e:
            print(e)


def usage(argv):
    cmd = path.basename(argv[0])
    print('usage: %s <from file> <to file>'
          '(example: "%s ./partner-links.json ./partner-links-checked.json")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 3:
        usage(argv)
    from_file = argv[1]
    to_file = argv[2]
    checker(from_file, to_file)
