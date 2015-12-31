#!/usr/bin/python

import random

from file_utilities import train_from_file, save_whole, save_parts, parse_dp
from features import construct_stacks, combined_feature
from ArcEager import NonProjectiveParseError, ArcEagerState

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

	surprisal_parser.add_argument("--dp_file", nargs='+')
	surprisal_parser.add_argument("--wts_file", nargs='+')
	surprisal_parser.add_argument("--trans_file")
	surprisal_parser.add_argument("--surp_file", nargs='+', default='surp.txt')
	surprisal_parser.add_argument("--k", nargs='+', type=int, default=[3])
	surprisal_parser.add_argument("--num_sent", type=int, default=None)

	args = parser.parse_args()
	random.seed(0)
	# print args

	if args.subparser_name == 'process':

		logs_list = []
		sent_list = []
		for ifile in args.ifiles:
			logs, sens = train_from_file(ifile, args.file_type)
			logs_list += logs
			sent_list += sens
		os.chdir(args.dir)
		print ArcEagerState.transition_codes
		save_whole(args.ofile, logs_list)
		if args.n:
			save_parts(args.ofile, args.n, logs_list, sent_list)
		os.chdir(script_dir)

	elif args.subparser_name == 'surprisal':
		
		ArcEagerState.recover_transitions(args.trans_file)
		for k in args.k:
			correct, correct_label, total, gold_trans = 0,0,0,0
			for dp_file, wts_file, surp_file in zip(args.dp_file, args.wts_file, args.surp_file):
				ct = parse_dp(dp_file, wts_file, surp_file, k, num_sent=args.num_sent)
				correct += ct[0]
				total += ct[1]
				gold_trans += ct[2]
				correct_label += ct[3]
			print "UAS = %.2f%%, LAS = %.2f%% and gold transition availability = %.2f%% on %d tokens with k=%d"%(100.0*correct/total, 100.0*correct_label/total, 100.0*gold_trans/(total), total, k)	
			print ""
		os.chdir('../scripts')

	
