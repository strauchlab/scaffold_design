## scaffold_design

data and examples from our manuscript:

"Sampling of Structure and Sequence Space of Small Protein Folds"



### installation requirements for backbone and sequence design:

* Rosetta licence

* PyRosetta installation

* Psipred, if you would like to use secondary structure predictions during design and for rescoring (we recommend). 

* for faulty fragments as a filter you will need filtered 4mers (under input)

* for pair motifs, you will need the pair motif database (under input)

* Anaconda2 (or select skilearn packages, see header of prediction code)


### content: ###

#### under examples:

* example for backbone design. Contains script to generate command line and how to design the folds
  reported in the manuscript. There are also all XMLs used for the generation of the reported folds in the paper.

* example for sequence design. The two different protocols can be found in two different folders along with a script to generate the commandlines.
  Also starting input (several backbones generated through the above XML script)

#### data:

* contains the stability data information and sorting details

#### predictions:

* contains summary of all scores

* prediction code in form of a jupyter notebook

* example scoring based on data from the Rocklin et all. data set
