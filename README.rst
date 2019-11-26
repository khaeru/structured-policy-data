Structured data on climate & energy policies
============================================

© 2019 Paul Natsuo Kishimoto <mail@paul.kishimoto.name>.
Licensed under `CC BY-SA <http://creativecommons.org/licenses/by-sa/4.0>`_.


This repository contains an example of how to use structured data formats to
store policy data.


Good data structures should be:

- **Human-readable and -editable.**

  - Free of visual clutter; unused fields may be, and are, omitted.

  - Structured: the layout of the data (within files, the names of files,
    their organization) helps users find certain data.

  - Contain recognizable symbols; terms that are self-explanatory for the
    intended users; and values from clearly-defined lists.

    - The reference code *should* include tools to check this information.

  - In parsimonous formats that are not laborious to edit.

  ...but **also**...

- **Machine-readable.**

  Code is provided:

  - ...that reads and writes the data in the standard format (essential).

    - Data that can be read by this 'reference' code is valid data.

    - Data that cannot be read is not in the proper format.

    - The reference code should itself be simple and easy to read,
      well-commented, and tested.

  - ...in multiple programming languages (optional; users can write their own
    by translating the reference code).

  - ...that reads and writes the data in other formats (optional).

  - ...that prepares model input data based on the data structures (optional;
    modeling teams can write their own, as one way of expressing their
    methodology).

  The structures should also be versionable. Usually, this means text-mode
  files, so that reliable, popular, well-supported tools like git can be used
  to store changes to the files, and display information about those changes.


Terminology
-----------

- The unit of observation is a *policy*.
- *Fields* in the data are *measures* or *indicators* of abstract or background
  *concepts*.
- Their values can take a variety of forms:

  - Numbers.
  - Symbols or text in specific formats or from certain lists.
  - Widely-known formats such as URLs, e-mail addresses, etc.
  - Free text of (un)limited length.
  - Other structured sub-units of observation, e.g. *targets* associated with a
    policy, or *jurisdictions* to which it applies.


Example
-------

The example is provided using YAML formatted files and Python code; other
formats and languages/frameworks could be used. Provided are:

- Three files with a selection of rows from three different policy databases:
  ``new-climate.yaml``, ``cd-links.yaml``, and ``commit.yaml``.
- A metadata file ``structure.yaml`` with code lists.
- Code (``example.py`` and ``structure.py``) that reads the files and
  manipulates them, demonstrating:

  1. Defining data structures in code (in ``structure.py``).
  2. Reading from various formats to a common structure (in ``example.py``).
  3. Writing to a common format (in ``example.py``).


Further steps
-------------

One optional item listed above is “code that prepares **model input data**
based on the data structures.” From the example given, the steps to prepare
input data for a global integrated assessment model (IAM) might be:

1. Iterate over a list of ``Policy`` objects, selecting and/or discarding them
   based on their attributes.
2. Associate the objects, based on their ``.coverage`` attribute (=list of
   jurisdictions covered by the policy), with model regions.
3. Use the ``.targets`` attribute of the object to retrieve the data about the
   targeted variable, value(s), unit, and year(s).
4. Apply methods to aggregate #3 to the level of #2.
5. Combine #4 with existing model data or reference/input data to produce
   model input data.

   - This could optionally be dumped to a file like an MS Excel spreadsheet, as
     well as entering the model.

The example stores coverage/**jurisdiction** data as a *list* of *'::'-delimited
strings*; for instance::

    coverage:
    - 'Country :: DEU'

This could be extended to cover a variety of types of jurisdictions::

    coverage:
    - 'City :: AUT :: Vienna'
    - 'Country group :: ENGAGE :: R14_WEU'
    - 'Country group :: COMMIT :: High-income countries'
    - 'Industry :: Maritime shipping'  # e.g. for IMO targets

As elsewhere, the code should operate based on lists that definine allowable
values. The existing lists in ``structure.yaml`` should be expanded to
include definitions of the items and reduce duplication.
