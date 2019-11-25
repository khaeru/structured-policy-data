"""1. Data structures. --------------------------------------------------------

Two things are demonstrated here:

- Lists of valid codes are read from a file, structure.yaml. A well-defined
  format will include an official, versioned structure definition and code to
  read it. The defintion will include not just the short names (as here), but
  verbose descriptions of each item.

- A Python package called 'pydantic' is used to enforce objects (=units of
  observation) with specific attributes (=fields for concepts) in particular
  types (=indicators and measures of the concepts). Again, only an example;
  others could be used.

  Read the class 'Policy' first, then 'Jurisdiction' and 'Target'.

"""
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import pycountry
import pydantic
from pydantic import AnyUrl
import yaml


# Read code lists
CODES = yaml.safe_load(open('structure.yaml'))

# Built-in Python enumeration object using codes from a list in a file
Sector = Enum('Sector', CODES['sector'])
ImplementationState = Enum('ImplementationState',
                           CODES['implementation state'])
Instrument = Enum('Instrument', CODES['instrument'])


class Target(pydantic.BaseModel):
    """Representation of a 'target': quantitative expression of a policy.

    The New Climate MS Excel format has columns titled
    "ImpactIndicatorSubObject"; in the example used here, these are all empty,
    but map to these fields.
    """
    # Single value for the target. Mutually exclusive with 'range'; a full
    # implementation would prevent both being set at once.
    value: float = None

    # Range of values for the target. Mutually exclusive with 'value'.
    range: Tuple[float, float] = None

    # Units for the value
    unit: str

    # Description of the quantity for which the value and units apply.
    quantity: str

    # Policy target date
    year: Optional[int]

    # Policy reference date
    reference_year: Optional[int]

    def as_dict(self):
        return filter_empty({
            'quantity': self.quantity,
            'year': self.year,
            'reference year': self.reference_year,
            'value': self.value,
            'range': self.range,
            'unit': self.unit,
        })


class Jurisdiction(pydantic.BaseModel):
    """The country or other entity to which a policy applies."""
    # Type of the jurisdiction. A full data model would use a list of codes.
    kind: str = 'country'

    # Information about the jurisdiction.
    info: Any = None

    def __init__(self, country_name):
        """Helper using a country name."""
        super().__init__()
        self.info = pycountry.countries.get(name=country_name)


class Policy(pydantic.BaseModel):
    # Policy name; the official name, if possible.
    name: str = None

    # Sector(s). Here, the enumeration is used, so this attribute may only take
    # the enumerated values. Other values will cause the code to error, drawing
    # attention to the flawed data.
    sector: List[Sector] = []

    # Instrument and state, also using enumerations
    instrument: List[Instrument] = []
    state: ImplementationState = None

    # Jurisdictions covered by the policy.
    coverage: List[Jurisdiction] = []

    # Description of the policy or comment on the data provenance; one or
    # more sentences.
    description: str = None

    # Mapping from target labels to target observations.
    targets: Dict[str, Target] = {}

    # Source of policy information.
    source: Union[AnyUrl, str] = None

    def as_dict(self):
        """Convert Policy object to Python dict() for serializing as YAML."""
        result = dict(
            name=self.name,
            sector=list(map(lambda e: e.name, self.sector)),
            instrument=list(map(lambda e: e.name, self.instrument)),
            state=getattr(self.state, 'name', None),
            source=str(self.source),
            description=self.description,
        )

        # Process coverage
        try:
            country_code = self.coverage[0].info.alpha_3
            result['coverage'] = [f'Country :: {country_code}']
        except IndexError:
            # No Jurisdictions listed
            country_code = None

        # Process targets
        result['targets'] = {label: t.as_dict()
                             for label, t in self.targets.items()}

        # Remove null values and return
        return filter_empty(result), country_code


def filter_empty(values):
    """*values* is a dict; strip any 'None' or length-0 list or dict."""
    return {k: v for k, v in values.items()
            if not ((v is None)
                    or (isinstance(v, (list, dict)) and not len(v)))}
