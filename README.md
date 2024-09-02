# Platoon in Manufacturing

Integrating platoon-based techniques within smart manufacturing systems


Link to the research article will be available after submission


## User guide
The main point of this work is the integration between Netlogo and Python to make a smart manufacturing system evolve over time, while retrieving data from Netlogo, sending them to Python in order to perform computations, provide control actions and finally send them back to Python.

To launch the simulation, it is required:
- Python (version 3.9.7 is being currently used)
- Netlogo (version 6.2.2 is being currently used) at https://ccl.northwestern.edu/netlogo/download.shtml
-  **pynetlogo** library (more instruction at: https://pynetlogo.readthedocs.io/en/latest/install.html)

### How to launch an instance of simulation
A simulation can be launched by running _main.py_, which handles the creation of a Netlogo instance and provide a function to make it interact with the Python scripts.
In _NetlogoCommunicationModule.py_ a list of functions is present in order to retrieve and command values from and to Netlogo. It will be updated together with the development of the project, to have the most complete list of commands and enhance the interaction between the two environments.


### Where to exchange information between Python and Netlogo
In the _main.py_ file, the endless ```for``` loop is used to command the evolution of the system over time. 20 ticks (i.e. 20 iterations) are equivalent to one second of simulation. Inside this loop, you can add the desired function from the _NetlogoCommunicationModule.py_ in order to retrieve information from Netlogo or to command instructions to Netlogo. Values retrieved should be stored in the proper structures (i.e. AGV, Product, Machine, and Station classes). Each class has its own list of attributes and methods.

#### Which parameters need to be tuned
In _main.py_:
- **safety_distance**: minimum distance between AGVs below which the controller for the emergency maneuvers must be used
- **setup_time**: time needed to switch from one unloading process to the following one, used to ensure that the AGV will arrive at the unloading unit only when it becomes available from the previous unloading

In _potentialField_controller.py_:
- **attraction gain**: gain for the attraction force used when calling _calculate_attractive_force_
- **static_gain, dynamic_gain**: gains for the repulsive force (specifically, for static and dynamic obstacles) used when calling _calculate_repulsive_force_moving_obstacles_
- **safe_distance**: distance between obstacles to consider in the computation of the repulsive force, used when calling _calculate_repulsive_force_moving_obstacles_

In _AGV.py_:
- **Kr, Ka, Kb gains**: gains for the decision-making process regarding recharging scheduling
