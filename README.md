# Playrix Testing Task

The Playrix test task implementation. Includes a CLI utility generating and 
parsing random archives with information about game objects.


## Project Structure

The following modules are included:
1. `playrix/generate.py` - utilities to generate random XML files and archives;
2. `playrix/parse.py` - parsing generated XML archives;
3. `playrix/utils.py` - additional helpers;
4. `cli.py` - command-line interface to invoke generating and parsing commands.

To test the implementation of main project's classes, one could use 
[tox](https://tox.readthedocs.io/en/latest/) automation tool. Using `tox`, you 
only need to navigate into project's folder and run:
```bash
$ cd playrix 
$ tox
``` 

## Commands

To generate a bunch of archives with XML files, use:
```bash
(venv) $ python cli.py generate 100 archives
```

To parse a directory with generated archives:
```bash
(venv) $ python cli.py parse archives output
``` 

## Implementation Details

The core library used in the project is `lxml`. The library allows to generate 
XML trees in object-oriented fashion and save them into text files.

The `click` library allows to build sophisticated hierarchical command-line
interfaces. It is not really required in our case of a simple project with only
two commands, and a couple of available options but in general, the library is
very powerful and convenient tool.

The `Pandas` library (and its dependencies) is only used to save information
into CSV format. We could use built-in `csv` library instead because our data 
processing code is quite simple.

Finally, the `pytest` library is used to run test suits. 


## Further Improvements

To gain a computation speed-up, one could write critical fragments of the code 
with [Cython](http://cython.org), or use `numpy` arrays and random 
distributions to make the generation process a bit faster.
