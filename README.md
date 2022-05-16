# Proof of Concept catalog zones for NSD

These python scripts implement (Proof of Concept) catalog zones as specified in https://datatracker.ietf.org/doc/draft-ietf-dnsop-dns-catalog-zones.
The implementation builds upon the *zone verification* feature of NSD.
This feature has not yet been released, but is expected to be available in June 2022.
For the time begin the feature is available in this branch on github: https://github.com/NLnetLabs/nsd/tree/features/credns
A good description of the feature can be found in the README of the feature branch, here: https://github.com/NLnetLabs/nsd/blob/features/credns/doc/README#L771

# NSD as catalog zone consumer

Zone verification needs to be enabled globally like this:

```
verify:
	enable: yes
	verify-zones: no
```

A catalog zone (for example `catalog1`) from which zones will be added and deleted can then be configured as follows:

```
zone:
	name:		"catalog1"
	verify-zone:	yes
	verifier:	catalog-zone-consumer.py pattern4catalog1
```

The `catalog-zone-consumer.py` script (from this repo) needs to be in NSD's working directory (default is `"/etc/nsd"`).
The script assumes the `zonelistfile:` to be `"/var/db/nsd/zone.list"`.
If your `zonelistfile:` is located elsewhere you have to edit `catalog-zone-consumer.py` to change that value.

Zones will be added with the configuration specified in the pattern which is given as first argument to the `catalog-zone-consumer.py` script.
In the example above all added zones will be configured with pattern `pattern4catalog1`.

# Producing a catalog with NSD

The `nsd-catz-add.py` and `nsd-catz-del.py` scripts can be used to produce a catalog zone.
They are not dependant on the zone verification feature and can be used with regular mainstream NSD.
The scripts expects two arguments.
The first argument is the name of the pattern with which the new zone in the catalog is configured.
The second argument is the zone to be added or deleted.
The first argument is also the name of the catalog zone.
Furthermore, the scripts expect the catalog zone to be in the current directory.
These scripts also assume `zonelistfile:`

