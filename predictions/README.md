
notebooks for training and predicting stability

Rescoring steps:

1. rescore decoys with rescore16.xml and the Rosetta version defined in manuscript 
	(can be found under evaluation folder)

2. evaluate connectivity and energetic terms using the evaluate_connectivity script
	(can be found under evaluation folder)

3. combine scores using the combine_scores.ipynb
	(in this folder)


the classifier for prediction can be found in the classifier folder in this directory


