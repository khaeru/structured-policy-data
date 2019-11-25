"""Reading and manipulating shared policy data."""
from pathlib import Path

import yaml

from structure import (
    ImplementationState,
    Instrument,
    Jurisdiction,
    Policy,
    Sector,
    Target,
)


"""2. Reading from various formats to a common structure ----------------------

These examples read from YAML formats, but could equally read from MS Excel or
CSV files, scrape the web, etc.
"""

all_policies = []

# Read New Climate database policies from file, one by one
for p in yaml.safe_load(open('new-climate.yaml')):
    # Child dictionary for convenience
    pp = p['Policy']

    # Create the Policy object
    policy = Policy(
        name=pp['Name of policy'],

        # Split the sectors by ', '
        sector=[Sector[s] for s in pp['Sector name'].split(', ')],

        instrument=[Instrument[i] for i in
                    pp['Type of policy instrument'].split(', ')],
        state=ImplementationState[pp['Implementation state']],

        # NB this assumes Jurisdiction == 'Country', and only one country
        coverage=[Jurisdiction(pp['Country'])],

        source=pp['Source or references'],
    )

    # No targets

    # Store the object
    all_policies.append(policy)


# Read CD-LINKS policies
for p in yaml.safe_load(open('cd-links.yaml')):
    policy = Policy(
        # no name
        sector=[Sector[p['Sector']]],
        coverage=[Jurisdiction(p['Country'])],
        source='CD-LINKS database',
    )

    # Read a single Target
    t = Target(
       quantity=p['Variable'],
       unit=p['Unit'])

    # Store dates
    try:
        t.year = p['End year']
    except KeyError:
        pass
    try:
        t.reference_year = p['Base year']
    except KeyError:
        pass

    # Store either the value or a range of values
    if 'Value' in p:
        t.value = p['Value']
    else:
        t.range = p['Range']

    # Store the target
    policy.targets['default'] = t

    all_policies.append(policy)


# Read COMMIT policies
for p in yaml.safe_load(open('commit.yaml')):
    policy = Policy(
        # no name
        sector=[Sector[p['Sector']]],
        source=f"COMMIT database / ‘{p['Source']}’ via Google Sheet "
               '“Bridging Scenario GPP list 24 October 2019_final”.',
        description=p.get('Comment General', None),
    )

    # Read and store *two* Targets
    target_common = dict(quantity=p['Variable'], unit=p['Unit'])
    policy.targets = dict(
        developed=Target(
            value=p['Developed Countries Value'],
            year=p['Developed Countries Year'],
            **target_common),
        developing=Target(
            value=p['Developing Countries Value'],
            year=p['Developing Countries Year'],
            **target_common),
        )

    all_policies.append(policy)


"""3. Writing to a common format ----------------------------------------------

We create a directory 'policies/' with all the rows in a common format; one
policy per file.

- Code for handling policies should be able to combine policies from multiple
  files and directories.
- The file and directory structure can then encode additional information.
- Version control systems like 'git' can then record, and easily display,
  when particular policies (=files) were added, modified, or removed.

"""
OUTPUT_PATH = Path('policies')
OUTPUT_PATH.mkdir(exist_ok=True)


# Write to file
counts = {'ZZZ': 0}
for p in all_policies:
    data, country_code = p.as_dict()

    # Determine the filename using the country code
    country_code = country_code or 'ZZZ'
    counts[country_code] = counts.setdefault(country_code, 0) + 1
    filename = f"{country_code}-{counts[country_code]:03}.yaml"

    yaml.dump(data, open(OUTPUT_PATH / filename, 'wb'), encoding='utf-8',
              width=78, allow_unicode=True)
