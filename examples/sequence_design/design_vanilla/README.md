
## How to set up multiple design jobs with multiple PDBS

Requirement:
- clustered fragment library (4mers) for the faulty fragments filter
- psipred to predict secondary structure, and allow penalizing disagreement with intended secondary structure and predicted secondary structure. This is a third party program, and needs to be obtained elsewhere. However, there is a github. 
Both filters are currently turned off in the protocol


### make PDB list

find ../input_pdbs -name "*pdb" > pdbs.list

### generate a job for each pdb
Edit the job generation script to point at the Rosetta executable, then run.
For trouble shooting, erase the "mute all" command. However, we recommend not run many
jobs unmuted as the tracer output generates large files quickly.
How to run: 

bash generate_design_job.sh pdbs.list xmls/protocol.xml




