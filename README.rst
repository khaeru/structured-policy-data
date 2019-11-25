Structured data on climate & energy policies
--------------------------------------------

Good data structures should be:

- **Human-readable and -editable.**

  - Free of visual clutter; unused fields are be omitted.

  - Structured: the layout of the data should convey information about its
    organization.

  - Contain recognizable symbols; terms that are self-explanatory for the
    intended users; and values from clearly-defined lists.

    - The reference code *should* include tools to check this information.

  - In parsimonous formats that are not laborious to edit.

- **Machine-readable.**

  Code is provided:

  - ...that reads and writes the data in the standard format (required).

    - Data that can be read by this 'reference' code is valid data; data that
      cannot be read is not in the proper format.

    - The reference code should be simple and easy to read itself.

  - ...in multiple programming languages (optional; users can write their own
    by translating the reference code).

  - ...that reads and writes the data in other formats (optional).

  - ...that prepares model input data based on the data structures (optional;
    modeling teams can write their own, as one way of expressing their
    methodology).

  The structures should also be versionable. Usually, this means text-mode
  files, so that reliable, popular, well-supported tools like git can be used
  to store changes to the files and


Terminology
-----------

- The unit of observation is a *policy*.
- *Fields* in the data are *measures* or *indicators* of abstract or background
  *concepts*.
- Their values can take a variety of forms:

  - Numbers.
  - Symbols or text in specific formats or from certain lists.
  - Widely-known formats such as URLs, e-mail addresses, etc.
  - Free text of a limited length.


Example
-------

The example is provided using YAML formatted files and Python code; other
formats and languages/frameworks could be used.

Provided:

- Three files with a selection of rows from three different policy databases.
- A metadata file 'structure.yaml' with code lists.
- Code ('example.py' and 'structure.py') that reads the files and manipulates
  them, demonstrating:

  1. Defining data structures in code (in 'structure.py').
  2. Reading from various formats to a common structure.
  3. Writing to a common format.
