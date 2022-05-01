### Steps to train Rainbow (Reinforcement Learning)

This folder contains code to train an RL agent to play Space Invaders (an Atari game). We make use 
of Deep Q-Networks for Reinforcement Learning.

### Dependencies

#### ROMs
Download `Roms.rar` from the [Atari 2600 VCS ROM Collection](http://www.atarimania.com/rom_collection_archive_atari_2600_roms.html) and extract the downloaded RAR file. Then, run the following:

>python -m atari_py.import_roms <path to folder>

This should print out the names of ROMs as it imports them. The ROMs will be copied to your `atari_py` installation directory.

### Command to run 

>sh run.sh

The above command trains the model using AdaBelief as the optimizer, to make use of 
Adam comment Line 47 and uncomment Line 48 in [agent.py](./agent.py).

### Results
We provide results for Adam in ```results/adam_run``` folder and results for AdaBelief in ```results/adabelief_run``` folder.
