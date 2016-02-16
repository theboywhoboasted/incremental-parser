# incremental-parser
An Incremental Dependency Parser intended to get surprisal values

To run the parser, you need the files:
	ArcEager.py:		Implements the Arc Eager algorithm (can be replaced by any other incremental dependency parse algorithm)
	DependenyParse.py: 	The main function implemented here is best_parse which calulates likelihoods and surprisal
	file_utilities.py:	Implements mundane functions for file  handling
	maxent.py:		Implements prediction using megam weights (can be replaced by any standard model for prediction)
	features.py:		Contains the feature set to be used for training or prediction
	main.py:		Contains the main wrapper to run the parser



To run the parser:

In process mode (to get transitions):
	./main.py process [--dir DIRECTORY_WHERE_PROCESSING_SHOULD_BE_DONE] --ifiles IFILE_1 [IFILE_2 IFILE_3 ...] --ofile FILE_TO_SAVE_FEATURES_IN --file_type FILE_TYPE --feature_set FEATURE_SET
# file type can be conll, conllu or dp

In the surprisal mode:
	./main.py surprisal --dp_file DP_FILE_CONTAINING_SENTENCES --wts_file WEIGHTS_FILE --ofile NEW_CONLL_FILE --meta_file FILE_WITH META_DATA--surp_file FILE_TO_SAVE_SURPRISAL_VALUES --k K
# k can be any integer greater than 0


For code review:
Important components of code, that might have an error are in ArcEager.py and the best_parse function in DependencyParse.py

For more help:
See the file commands which contains the commands I used for coomon tasks.

          dfco1.V4  dfco2.V4  dfco3.V4  dfst1.V4  dfst2.V4
dfco1.V4 1.0000000 0.8993188 0.8695091 0.3308183 0.4153940
dfco2.V4 0.8993188 1.0000000 0.9807349 0.3610469 0.4679595
dfco3.V4 0.8695091 0.9807349 1.0000000 0.3566475 0.4653460
dfst1.V4 0.3308183 0.3610469 0.3566475 1.0000000 0.8912425
dfst2.V4 0.4153940 0.4679595 0.4653460 0.8912425 1.0000000


