from collections import defaultdict
from os import path
import json

partner_links = defaultdict(lambda: {
    'partner_link': 'https://gotbest.by/redirect/cpa/o/q5js2p2ydyw59iek0i7xeyug0in4ui24/',
    'partner_offers': ['https://s.click.aliexpress.com/e/LyULXZde?af=3722256&cv=38055532&cn=43q6mb7qaopi4qpa0ra6szn9ek94vc6o&dp=v5_43q6mb7qaopi4qpa0ra6szn9ek94vc6o&dl_target_url=https%3A%2F%2Faliexpress.ru%2Fitem%2F4000527624853.html%3Faf%3D3722256%26cv%3D38055532%26cn%3D43q6mb7qaopi4qpa0ra6szn9ek94vc6o%26dp%3Dv5_43q6mb7qaopi4qpa0ra6szn9ek94vc6o&afref=']
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