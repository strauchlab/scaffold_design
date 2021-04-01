
## How to set up multiple design jobs with multiple PDBS

Requirement:
- pair motif database (part of this github repository)
- clustered fragment library (4mers) for the faulty fragments filter (part of this github)
- psipred to predict secondary structure, and allow penalizing disagreement with intended secondary structure and predicted secondary structure. This is a third party program, and needs to be obtained elsewhere. However, there is a github. 
Both filters are currently turned off in the protocol


### make PDB list

find ../input_pdbs -name "*pdb" > pdbs.list

### generate a job for each pdb
Edit the file to point out the Rosetta executable 

bash generate_design_job.sh pdbs.list xmls/protocol.xml




