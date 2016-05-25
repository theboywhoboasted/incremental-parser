#!/usr/bin/python

import random

from file_utilities import train_from_file, save_whole, save_parts, parse_dp
from ArcEager import ArcEagerState

if __name__ == "__main__":
	import os, argparse

	script_dir = os.getcwd()
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(dest='subparser_name', help='different commands: process, surprisal')

	process_parser = subparsers.add_parser('process', help='process conll/dp/conllu file')
	surprisal_parser = subparsers.add_parser('surprisal', help='parse and compute surprisal')

	process_parser.add_argument("--ifiles", nargs='+', default=["../utf8/train/train-htb-ver0.51.gold.utf8.conll"])
	process_parser.add_argument("--dir", default='../hindi/features')
	process_parser.add_argument("--ofile", default="hindiPOSStacksNext.txt")
	process_parser.add_argument("--n", type=int, default=0)
	process_parser.add_argument("--file_type", default="conll")
	process_parser.add_argument("--labelled", default='False')
	process_parser.add_argument("--feature_set", default='combined_feature')

	surprisal_parser.add_argument("--dp_file", nargs='+')
	surprisal_parser.add_argument("--wts_file", nargs='+')
	surprisal_parser.add_argument("--meta_file", required=True)
	surprisal_parser.add_argument("--surp_file", nargs='+', default='surp.txt')
	surprisal_parser.add_argument("--k", nargs='+', type=int, default=[3])
	surprisal_parser.add_argument("--ofile", nargs='+')
	surprisal_parser.add_argument("--num_sent", type=int, default=None)

	args = parser.parse_args()
	random.seed(0)
	print args

	if args.subparser_name == 'process':

		logs_list = []
		sent_list = []
		ArcEagerState.state_func_name = args.feature_set
		ArcEagerState.labelled = True if (args.labelled == 'True') else False
		for ifile in args.ifiles:
			logs, sens = train_from_file(ifile, args.file_type)
			logs_list += logs
			sent_list += sens
		os.chdir(args.dir)
		print ArcEagerState.transition_codes
		save_whole(args.ofile, logs_list, args.labelled, args.feature_set)
		if args.n:
			save_parts(args.ofile, args.n, logs_list, sent_list)
		os.chdir(script_dir)

	elif args.subparser_name == 'surprisal':
		
		ArcEagerState.recover_metadata(args.meta_file)
		for k in args.k:
			correct, correct_label, total, gold_trans, correct_trans_avlbl, all_correct, all_correct_total, correct_sents, num_sents = 0,0,0,0,0,0,0,0,0
			for dp_file, wts_file, surp_file, ofile in zip(args.dp_file, args.wts_file, args.surp_file, args.ofile):
				stats = parse_dp(dp_file, wts_file, surp_file, k, ofile, num_sent=args.num_sent)
				correct += stats['correct']
				total += stats['total']
				correct_trans_avlbl += stats['correct_trans_avlbl']
				all_correct += stats['all_correct']
				all_correct_total += stats['all_correct_total']
				correct_label += stats['correct_label']
				correct_sents += stats['sent_correct']
				num_sents += stats['num_sents']
			print "UAS = %.2f%%, LAS = %.2f%% on %d tokens"%(100.0*correct/total, 100.0*correct_label/total, total)
			print "Sentence level accuracy = %.2f on %d sentences"%(100.0*correct_sents/num_sents, num_sents)
			print "Gold transition availability = %.2f%%"%(100.0*correct_trans_avlbl/(total))
			print "Gold parse availability = %.2f%% on %d truncations with k=%d"%(100.0*all_correct/all_correct_total, all_correct_total, k)	
			print ""

	
