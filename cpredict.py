import sys
sys.path.append('../code2vec')

import traceback
from common import common
from extractor import Extractor
from common import Config, VocabType
from argparse import ArgumentParser
from model import Model
from cextractor import file2function_array
import tensorflow as tf

if __name__ == '__main__':
    parser = ArgumentParser()
    usage = 'Usage: python {} [-l] file'\
            .format(__file__)
    parser = ArgumentParser(usage=usage)
    parser.add_argument('filename', type=str,
                        help='input file')    
    parser.add_argument("-d", "--data", dest="data_path",
                        help="path to preprocessed dataset", required=False)
    parser.add_argument("-te", "--test", dest="test_path",
                        help="path to test file", metavar="FILE", required=False)

    is_training = '--train' in sys.argv or '-tr' in sys.argv
    parser.add_argument("-s", "--save", dest="save_path",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument("-w2v", "--save_word2v", dest="save_w2v",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument("-t2v", "--save_target2v", dest="save_t2v",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument("-l", "--load", dest="load_path",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument('--save_w2v', dest='save_w2v', required=False,
                        help="save word (token) vectors in word2vec format")
    parser.add_argument('--save_t2v', dest='save_t2v', required=False,
                        help="save target vectors in word2vec format")
    parser.add_argument('--export_code_vectors', action='store_true', required=False,
                        help="export code vectors for the given examples")
    parser.add_argument('--release', action='store_true',
                        help='if specified and loading a trained model, release the loaded model for a lower model '
                             'size.')
    args = parser.parse_args()

    funcs = file2function_array(args.filename)

    # build up hash to path dict
    h2p_dict = {}
    for f in funcs:
        h2p_dict.update(f.get_pathdict())

    with tf.device('/cpu:0'):
        config = Config.get_default_config(args)
        model = Model(config)
        results, code_vector = model.predict([f.to_str_with_padding() for f in funcs if f.has_pair()])

    prediction_results = common.parse_results(results, h2p_dict)

    for method_prediction in prediction_results:
        print('Original name:\t' + method_prediction.original_name)
        for name_prob_pair in method_prediction.predictions:
            print('\t(%f) predicted: %s' % (name_prob_pair['probability'], name_prob_pair['name']))
        print('Attention:')
        for attention_obj in method_prediction.attention_paths:
            print('%f\tcontext: %s,%s,%s' % (
            attention_obj['score'], attention_obj['token1'], attention_obj['path'], attention_obj['token2']))
            
    model.close_session()
