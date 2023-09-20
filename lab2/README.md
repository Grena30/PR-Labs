# Lab 2: Serialization.
## Task:

Create a players factory class that will be able to convert different serializable formats into player class and backwards.

The [factory.py](https://github.com/ScienceKot/PR_LABS_TASKS/edit/main/LAB2/factory.py) is a class defined 
with 6 empty methods which need to be implemented: to_json, from_json, to_xml, from_xml, to_protobuf, from_protobuf.

The following files can be used as guide for implementations:
* players.json
* players.xml
* players.proto


The [tests.py](https://github.com/ScienceKot/PR_LABS_TASKS/edit/main/LAB2/tests.py) and [homework_test](...) files need to be used to test the implementations.

Sources: 
1. https://www.freecodecamp.org/news/googles-protocol-buffers-in-python/
2. https://stackoverflow.com/questions/11502113/how-to-get-top-level-protobuf-enum-value-name-by-number-in-python
3. https://www.programiz.com/python-programming/datetime/strftime
4. https://stackabuse.com/how-to-convert-json-to-a-python-object/
5. https://docs.python.org/3/library/xml.etree.elementtree.html