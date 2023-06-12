# Platoon in Manufacturing

Integrating platoon-based techniques withing smart manufacturing systems


Overleaf(Latex) project: https://www.overleaf.com/2212164663mhrbpfvqpwtn


## User guide
The main point of this work is the integration between Netlogo and Python to make a smart manufacturing system evolve overtime, while retrieving data from Netlogo, send them to Python in order to perform computations, provide control actions and finally send them back to Python.

To launch the simulation, you must install:
- Python (version 3.9.7 is being currently used)
- Netlogo (version 6.2.2 is being currently used) at https://ccl.northwestern.edu/netlogo/download.shtml
-  **pynetlogo** library (more instruction at: https://pynetlogo.readthedocs.io/en/latest/install.html)

### How to launch an instance of simulation
A simulation can be launched by running _main.py_, that handles the creation of a Netlogo instance and provide function to make it interact with the Python scripts.
In _NetlogoCommunicationModule.py_ a list of functions is present in order to retrieve and command values from and to Netlogo. It will be updated together with the development of the project, to have the most complete list of command and enhance the interaction between the two environments.


### Where to exchange information between Python and Netlogo
In the _main.py_ file, the endless ```for``` loop is used to command the evolution of the system overtime. 20 ticks (i.e. 20 iterations) are equivalent to one second of simulation. Inside this loop, you can add the desired function from the _NetlogoCommunicationModule.py_ in order to retrieve information from Netlogo, or to command instruction to Netlogo. Values retrieved should be store in the proper structures (i.e. AGV, Product, Machine and Station classes). Each class has its own list of attributes and methods.
