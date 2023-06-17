Konrad Weakley's Into to AI Project


#####Environment Details#####
Python Packages: matplotlib, imageio, numpy, Pillow
interpreter: 3.8 (most 3.x interpreters should work)
#############################


##### FOR EASE OF GRADING #####
- The "Final Frames and Gifs' Folder contains .gifs and .pngs with descriptive names for many different testcases
- cases tested: 
	- very short wi-fi range
	- very long wi-fi range
	- complete exploration of the environment (when possible and consistent)
	- large environment
	- differing numbers of robots
###############################


##### Running the Code ####################################
- make sure that the "mazepics" and "randomsquarepics" directories exist in the project directory
- after installing the required packages, simply use the command "python {file of choice}.py"
- both sqares.py and generatedRooms.py can be run this way
	squares.py: environment with randomly generated squares. 5 robots and a 50X50 environment by default
	generatedRooms.py: hardcoded environment that looks kind of like a maze, or a floorplan to a really bad house
- After running, the script will spit out a gif and image of the last frame, both with descriptive titles
###########################################################


###Modifiable constants###
- You can easily change the TIMESTEPS and NUM_ROBOTS variables to test different outputs
- The size of the environment in squares.py can be modified as well, but keep in mind not to make 
the environment too much smaller than the range of the robots or the code will not work (a 50x50 environment must have a range smaller than 150). 
I recommend only making small changes to this variable if you don't want to debug my code(10-30) or just make sure that the size of the diagonal is
less than (robot.RANGE * 3)
- The ROBOT range can be modified pretty easily, but be careful not to decrease it too much when running the generatedRooms.py script or the robots
will start outside the range of the base station
