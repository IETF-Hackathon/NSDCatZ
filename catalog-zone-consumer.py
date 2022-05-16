#!/usr/bin/env python3

zonelistfile = '/var/db/nsd/zone.list'
nsdcontrol = 'nsd-control'
#nsdcontrol = '/usr/local/sbin/nsd-control'

import os
import sys

if len(sys.argv) != 2:
    print("usage %s <catalog>" % sys.argv[0])
    sys.exit(1)

catalog = sys.argv[1].lower()

my_zones = set()
with open(zonelistfile, 'r') as zl:
    for ln in zl:
        if not ln.startswith('add'):
            continue
        
        add, zone, pattern = ln.split()
        if pattern == catalog:
            my_zones.add(zone.lower())

catzones = set()
process = False
for ln in sys.stdin:
    if ln[:-1] == '$ORIGIN zones.%s.' % catalog:
        process = True

    elif ln.startswith('$ORIGIN'):
        process = False

    elif process:
        pieces = ln[:-1].split('\t')
        if pieces[3] != 'PTR':
            continue
        if '.' in pieces[0]:
            continue
        catzones.add(pieces[4][:-1].lower())

print('Deleting zones: %s' % ' '.join(my_zones - catzones))
for zone in my_zones - catzones:
    os.system(nsdcontrol + ' delzone %s' % zone)

print('Adding zones: %s' % ' '.join(catzones - my_zones))
for zone in catzones - my_zones:
    os.system(nsdcontrol + ' addzone %s %s' % (zone, catalog))

