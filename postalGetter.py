import requests
import time
from multiprocessing import Pool

def pcode_to_data(pcode):
    page = 1
    results = []
    
    while True:
        try:
            response = requests.get('http://developers.onemap.sg/commonapi/search?searchVal={0}&returnGeom=Y&getAddrDetails=Y&pageNum={1}'
                                    .format(pcode, page)) \
                               .json()
        except requests.exceptions.ConnectionError as e:
            print('Fetching {} failed. Retrying in 2 sec'.format(pcode))
            time.sleep(2)
            continue
            
        results = results + response['results']
    
        if response['totalNumPages'] > page:
            page = page + 1
        else:
            break
            
    return results

import json

if __name__ == '__main__':
    pool = Pool(processes=5)
    
    postal_codes = range(99000, 100000)
    postal_codes = ['{0:06d}'.format(p) for p in postal_codes]

    all_buildings = pool.map(pcode_to_data, postal_codes)
    all_buildings.sort(key=lambda b: (b['POSTAL'], b['SEARCHVAL']))

    jstr = json.dumps([y for x in all_buildings for y in x], indent=2, sort_keys=True)
    for p in jstr:
        new_data['postaldata'].append({
            'postal': p['POSTAL'],
            'x':p['X'],
            'y':p['Y']
            })
    with open('postalData.json', 'w+') as outfile:  
        json.dump(new_data, outfile)
 
