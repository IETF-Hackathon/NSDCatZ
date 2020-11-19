#!/usr/bin/env python3

import os
import sys
import uuid
from datetime import datetime

serial = int(datetime.now().strftime('%Y%m%d00'))

if len(sys.argv) != 3:
    print("usage %s <catalog> <zone>" % sys.argv[0])
    sys.exit(1)

catalog = sys.argv[1].lower()
new_zone = sys.argv[2]
if new_zone[-1] == '.':
    new_zone = new_zone[:-1]

with open(catalog, 'r') as c:
    for ln in c:
        ln = ln[:-1].split('\t')
        if ln[3] == 'SOA':
            cat_serial = int(ln[4].split()[2])

new_serial = serial if serial > cat_serial else cat_serial + 1
zones = set()
with open('/var/db/nsd/zone.list', 'r') as zl:
    for ln in zl:
        if not ln.startswith('add'):
            continue
        
        add, zone, pattern = ln.split()
        if pattern == catalog:
            zones.add(zone)

if 'add' in sys.argv[0]:
    if os.system('nsd-control addzone %s %s' % (new_zone.lower(), catalog)) != 0:
        sys.exit(1)
    else:
        zones.add(new_zone.lower())
elif new_zone.lower() not in zones:
    print('Zone %s not found in catalog %s\n' % (new_zone, catalog))
    sys.exit(1)
elif os.system('nsd-control delzone %s' % new_zone.lower()) != 0:
    sys.exit(1)
else:
    zones.remove(new_zone.lower())

with open(catalog, 'w') as c:
    c.write( '%s.\t0\tIN\tSOA\tinvalid. invalid. %d 3600 600 2419200 0\n'
           % (catalog, new_serial))
    c.write('%s.\t0\tIN\tNS\tinvalid.\n' % catalog)
    c.write('version.%s.\t0\tIN\tTXT\t"2"\n' % catalog)
    for zone in zones:
        c.write( '%s.zones.%s.\t0\tIN\tPTR\t%s.\n'
               % ( uuid.uuid5(uuid.NAMESPACE_DNS, zone), catalog, zone ))

os.system('nsd-control reload %s' % catalog)
print('%s: %s' % (catalog, ' '.join(sorted(zones))))
