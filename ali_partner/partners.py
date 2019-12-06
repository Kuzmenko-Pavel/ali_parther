from collections import defaultdict
from os import path
import json

partner_links = defaultdict(lambda: {
    'partner_link': 'https://gotbest.by/redirect/cpa/o/q1ogbz6jmp2fzxff8y2zht4ocxd0fh2n/',
    'partner_offers': ['https://ru.aliexpress.com/item/4000082655649.html']
})

json_path = path.join(path.dirname(path.abspath(__file__)), "partner-links.json")
with open(json_path) as json_file:
    try:
        data = json.load(json_file)
        for ix, item in enumerate(data, 1):
            partner_links[ix] = {
                'partner_link': item.get('partner'),
                'partner_offers': [item.get('sclick')]
            }
    except Exception as e:
        print(e)