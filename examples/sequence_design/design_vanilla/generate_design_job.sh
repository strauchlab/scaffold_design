#!/bin/bash

# simple bash script to make jobs for multiple pdbs
if [ -z $2 ]; then
  echo "USAGE: generate_design_job.sh <listwithpdbs> <protocol.xml> "
  exit
fi


protocol=$2
pdblist=$1

rosetta_exec="$HOME/Rosetta/main/source/bin/rosetta_scripts.linuxgccrelease" 

dir=`pwd`
protocol=$2
nstruct=1
ntrials=1
flags="  -parser:script_vars aa_comp=ala_trp_met.comp  -run:preserve_header 1 -no_his_his_pairE  -nblist_autoupdate true -chemical:exclude_patches LowerDNA UpperDNA Cterm_amidation SpecialRotamer VirtualBB ShoveBB VirtualDNAPhosphate VirtualNTerm CTermConnect sc_orbitals pro_hydroxylated_case1 pro_hydroxylated_case2 ser_phosphorylated thr_phosphorylated tyr_phosphorylated tyr_sulfated lys_dimethylated lys_monomethylated  lys_trimethylated lys_acetylated glu_carboxylated cys_acetylated tyr_diiodinated N_acetylated C_methylamidated MethylatedProteinCterm "


# -- Output File Prefix --
prefix="jobs"

# -- Output File Suffix --
suffix=".sub"


for i in `cat $pdblist`; do

	echo "$rosetta_exec  -nstruct $nstruct $flags  @flags -s $i -use_input_sc  -mute all -parser:protocol $dir/$protocol"   >> $prefix$file_num_format$suffix
	# >> $prefix$file_num_format$suffix
done


