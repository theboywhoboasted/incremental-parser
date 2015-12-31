# incremental-parser
An Incremental Dependency Parser intended to get surprisal values

To run the parser, you need the files:
	ArcEager.py:		Implements the Arc Eager algorithm (can be replaced by any other incremental dependency parse algorithm)
	DependenyParse.py: 	The main function implemented here is best_parse which calulates likelihoods and surprisal
	file_utilities.py:	Implements mundane functions for file  handling
	maxent.py:			Implements prediction using megam weights. Can be replaced by any standard model for prediction
	file_tasks.py (optional): Contains functions to do intermediate file processing. Not needed if you have data in the right form

To run the parser:

In process mode (to get transitions):
	./file_utilities.py process [--dir DIRECTORY_WHERE_PROCESSING_SHOULD_BE_DONE] --ifiles IFILE_1 [IFILE_2 IFILE_3 ...] --ofile FILE_TO_SAVE_WEIGHTS_IN --file_type FILE_TYPE

file type can be conll, conllu or dp

In the surprisal mode:

./file_utilities.py surprisal --dp_file DP_FILE_CONTAINING_SENTENCES --wts_file WEIGHTS_FILE --surp_file FILE_TO_SAVE_SURPRISAL_VALUES --k K

k can be any integer greater than 0

For code review:

Important components of code, that might have an error are in ArcEager.py and the best_parse function in DependencyParse.py

