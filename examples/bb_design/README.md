## How to design new backbone for a desired fold

1. change parameters in teh setup script, such as path for the Rosetta_scripts executable and 
	variables you might want to change dynamically through the script variable %%myvariable%% 
	the xml


2. run the setup script

python make_commandline.py

which will generate as many folder as you specified multiplied by the scripts variables
it will also create a commands file which has the Rosetta command line and all options set up

3. running Rosetta

just execute the commands file or load into your scheduling system:

bash commands

folder 0000 contains a sample run and sample output. The tracer was left "open" so we gzipped the file

