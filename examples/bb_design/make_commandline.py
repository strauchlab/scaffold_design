#!/usr/bin/python

import glob
import os
import math
import sys
import operator
import shutil,  subprocess
import re

#############################
### Options

# location of Rosetta_scripts executable
### ---> MODIFY <------ ###
exe = '/home/str/rosi/Rosetta/main/source/bin/rosetta_scripts.static.linuxgccrelease'
base_dir = '..'

# rosetta_scripts protocol file (the xml!)
### ---> MODIFY <------ ###
xml = os.path.join( base_dir, 'xmls/betagrasp-bb-generation.xml' )

#############################

# number of folders to generate
# each design trajectory needs to run in its own folder due to temporary output
f = 10 

#############################

def xml_vars_to_str( xml_vars ):
    options = [ '='.join( (vname, xml_vars[vname]) ) for vname in sorted(xml_vars.keys()) ]
    return ' '.join( [ ' '.join( ('-parser:script_vars', o) ) for o in options ] )

def condor_com(cdir):
    com = "Executable  = "+ cdir + '/run.sh\n'
    com += "transfer_executable = false\n"
    com += "universe    = vanilla\n"
    com += "Error       = "+ cdir + '/stderr.log\n'
    com += "Output      = "+ cdir + '/stdout.log\n'
    com += "Log         = " + cdir + '/condor.log\n'
    com += 'queue 1\n'
    return com

curr_dir =  os.getcwd()
cmds = []

##############################
### rosetta scripts variables

### ---> MODIFY if more variable for the rosetta script (xml) are desired <------ ###

# for instance position of a bulge
b_array = [2,4,5 ]


for j in range(f):
  for i in b_array :
	### list variables here! ###
    	xml_vars = {
        	'b' : str( i ) # bulge variables
    	}

    	input_pdb = os.path.join( base_dir, 'input/startingstub.pdb' )
        pid = '%04d' % (len(cmds) )

	### define Rosetta commandline extra options here that go beyond the standard #### 
        #subprocess.Popen( "mkdir " + pid,shell=True)
        cmd = [
            #'mkdir', '-p', pid, '&&',
            #'#!/bin/bash\n',
            'cd', pid, '&&',
            exe, '-s', input_pdb,
            '-mute all',
            '-parser:protocol', xml,
            '-nstruct', '100',
            '-out:suffix', '_' + pid,
            xml_vars_to_str( xml_vars ),
	    '>', 'stdout.log', ';',
            'cd', base_dir
        ]
        
        
        #filename = 'run.sh'
        cmds.append( ' '.join(cmd) )
        if not os.path.exists(pid): os.makedirs(pid)
        #f = open(pid + '/' + filename, 'w')
        #cmds.append(' '.join(cmd))
        #f.write(' '.join(cmd)) 
        #f.close()
        #outcondor = open( pid  + '/job.cdr' , 'w')	    
        #outcondor.write (condor_com(curr_dir + '/' + pid ))
        #subprocess.Popen( "chmod +x " + pid  + '/run.sh' ,shell=True)

## end sampling ##

## below not necessary for condor ##
filename = 'commands'
with open( filename, 'w' ) as f:
    f.write( '\n'.join( cmds ) )
print 'Wrote', len(cmds), 'commands to', filename


