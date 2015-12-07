import sys, re, os, ast
import gensim, logging

from streamer import Sentences
from phrasing import phrase_detection

from configobj import ConfigObj

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', format=logging.INFO)

def print_similars(model, item_list, N):
	print 'Top ' + str(N) + ' Items similar to:' + item_list
	for each in model.most_similar(item_list, [], N):
		print each

def test(model):
	#print model.most_similar_cosmul('BANGALORE', 'HYDERABAD', 10)
	print model.most_similar_cosmul(positive = ['java'])
	#print_similars(model, sys.argv[1], int(sys.argv[2]))

def train(model_name, is_phrased, input_data_dir, size, window, negative, sample, min_count, workers, iterations, out_model_file):

	print 'IsPhrased = ' + is_phrased
	data = Sentences(input_data_dir)

	model = gensim.models.Word2Vec(size=size, window=window, negative=negative, sample=sample, min_count=min_count, workers=workers, iter=iterations)
	model.build_vocab(data)
	
	T = model.train(data)

	model.save(out_model_file)
	print 'Model: ' + model_name + ' saved to disk in: [' + out_model_file + '.'

	print 'Model trained: ' + str(model)
	print 'Model vocab count ' + str(len(model.vocab))
	
	return model
	
def print_vocab(model):
	for each in model.vocab:
		print each
	print 'Vocab count: ' + str(len(model.vocab))

def train_model(config):

	model_name = config['word2vec']['model_name']

	print '########### Training word2vec model: ' + model_name

	model = train(model_name,
			config['word2vec']['train']['is_phrased'],
			config['word2vec']['train']['input_file'],
			int(config['word2vec']['train']['size']), 
			int(config['word2vec']['train']['window']),
			int(config['word2vec']['train']['negative']),
			float(config['word2vec']['train']['sample']),
			int(config['word2vec']['train']['min_count']),
			int(config['word2vec']['train']['workers']),
			int(config['word2vec']['train']['iterations']),
			config['word2vec']['train']['out_model_file'])
	return model

def test_model(config):
			
	model_name = config['word2vec']['model_name']

	print '########### Testing word2vec model: ' + model_name

	model = gensim.models.Word2Vec.load(config['word2vec']['test']['model_file'])
	test(model)


def phrasing(config):
	raw_in_file = config['preprocessing']['raw_in_file']

	print '#################### Phrase detection in: ' + raw_in_file
	phrase_detection(raw_in_file)

if __name__ == '__main__':

	config = ConfigObj('./config.ini')
	actions = config['main']['action']

	for action in actions.split(','):
		
		if   action == 'train':
			train_model(config)
		elif action == 'test':
			test_model(config)
		elif action == 'phrase':
			phrasing(config)
		else:
			print 'Invalid instruction in config file.'

