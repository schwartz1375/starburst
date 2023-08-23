## STARBURST
The concept is to build a script(s) that pull down [MITRE CTI - STIX 2.1](https://github.com/mitre-attack/attack-stix-data) and insert the data into a local database for offline access. 

## Adding Commercial Grade Context
A SQLite Database of MITRE ATT&CK STIX Data

Value Prop:  If we know the family (i.e. clop) we can provide:
* Malware family description
* Malware family TTPs
* When linked with [SWEETHONEY](https://github.com/schwartz1375/sweethoney/) we can also provide function TTPs

## Prototype Usage Example
First retrieve and load the database with the following command `python3 ./stix_db_loader.py`, then search the database via `python3 ./malware_technique_mapper.py <malware name>` to generate a enterprise malware family layer.  If the family exists it will create a file family_layer.json file.

``` 
(.env) starburst % python3 ./stix_db_loader.py
(.env) starburst % python3 ./malware_technique_mapper.py clop
Generated clop_layer.json successfully.
(.env) starburst % python3 ./malware_technique_mapper.py fakename
No malware found with name fakename.
```

## Resouces
* [MITRE ATT&CK Homepage](https://attack.mitre.org/)
* [CTI Python STIX 2](https://github.com/oasis-open/cti-python-stix2)
* [MITRE CTI - STIX 2.1](https://github.com/mitre-attack/attack-stix-data)
* [MITRE CTI - STIX 2.0](https://github.com/mitre/cti) 
* [mitreattack-python](https://github.com/mitre-attack/mitreattack-python)
* [Mitre-Attack-API](https://github.com/annamcabee/Mitre-Attack-API)
