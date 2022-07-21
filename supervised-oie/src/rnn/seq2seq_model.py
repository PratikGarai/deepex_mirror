""" Usage:
    seq2seq_model --train=TRAIN_FN --dev=DEV_FN --test=TEST_FN --hyperparams=MODEL_JSON --saveto=MODEL_DIR [-v]

Train a seq2seq OIE model.

Parameters:
  train                The train file
  dev                  The development file
  test                 The test file
  hyperparams          Json paramters to init model
  saveto               Where to store the trained model
  v                    Verbose
"""

import seq2seq
import pandas as pd
import numpy as np
from keras.utils import plot_model
from seq2seq.models import Seq2Seq, AttentionSeq2Seq
from keras.callbacks import LambdaCallback, ModelCheckpoint
from docopt import docopt
from pprint import pformat
import logging
import json

from load_pretrained_word_embeddings import Glove

class Seq2seq_OIE:
    """
    Modelling OIE as sequence to sequence, allows for introducing non-sentenial words into
    the predictions, and not having to align the tuples words.
    """
    def __init__(self,
                 **args):
        """
        Init and compile model's params
        Arguments:
        seed - the random seed to use
        sep - the delimiter to be used in the csv files
        batch_size - (=input_lenght) Batch size in which to partition the elements
        maximum_output_length - The maximum number of words in output
        emb - Pretrained embeddings
        hidden_dim - number of hidden units
        input_depth - the number of layers in encoder
        output_depth - the number of layers in decoder
        peek - (binray) add the peek feature
        attention - (binary) use attention model
        epochs - Number of epochs to train the model
        loss - (string) the loss function, one of keras options
        optimizer - (string) the optimizer function, one of keras options
        """
        self.args = args
        self.sep = str(self.args['sep'])
        self.emb = Glove(self.args['emb_fn'])
        self.epochs = self.args['epochs']
        np.random.seed(self.args['seed'])
        self.model = Seq2seq_OIE.compile_model(input_length = self.args['batch_size'],
                                               input_depth = self.args['input_depth'],
                                               input_dim = self.emb.dim,
                                               hidden_dim = self.args['hidden_dim'],
                                               output_length = self.args['maximum_output_length'],
                                               output_depth = self.args['output_depth'],
                                               output_dim = self.emb.dim,
                                               peek = self.args['peek'],
                                               attention = self.args['attention'],
                                               loss = self.args['loss'],
                                               optimizer = self.args['optimizer'],
        )


    @staticmethod
    def compile_model(input_length,
                      input_depth,
                      input_dim,
                      hidden_dim,
                      output_length,
                      output_depth,
                      output_dim,
                      peek,
                      attention,
                      loss,
                      optimizer
    ):
        """
        Returns a compiled seq2seq model
        Arguments:
        input_length - Batch size in which to partition the elements
        input_depth - the number of layers in encoder
        input_dim - the number of features for each word
        hidden_dim - number of hidden units
        output_length - (= maximum_output_length) The maximum number of words in output
        output_depth - the number of layers in decoder
        output_dim - the number of features in word embedding's output
        peek - (binray) add the peek feature
        attention - (binary) use attention model
        loss - (string) the loss function, one of keras options
        optimizer - (string) the optimizer function, one of keras options
        """

        # Only pass peek as an argument if using an attention model
        model_fn = lambda **args: \
                   AttentionSeq2Seq(**args) \
                   if attention \
                      else Seq2Seq(peek = peek, **args)

        model = model_fn(input_length = input_length,
                         input_dim = input_dim,
                         hidden_dim = hidden_dim,
                         output_length = output_length,
                         output_dim = output_dim,
                         depth = (input_depth,
                                  output_depth),
        )

        model.compile(loss = loss,
                      optimizer = optimizer)

        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            model.summary()
        return model

    def get_callbacks(self, X):
        """
        Returns callbacks listed below.
        X is the encoded dataset used to print a sample of the output.
        Callbacks created:
        1. Sample output each epoch
        2. Save best performing model each epoch
        """
        sample_output_callback = LambdaCallback(on_epoch_end = lambda epoch, logs:\
                                                pprint(self.sample_labels(self.model.predict(X))))
        checkpoint = ModelCheckpoint(os.path.join(self.model_dir,
                                                  "weights.hdf5"),
                                     verbose = 1,
                                     save_best_only = False)   # TODO: is there a way to save by best val_acc?
        return [sample_output_callback,
                checkpoint]


    def train(train_fn, dev_fn):
        """
        Train this model on a given train dataset
        Dev test is used for model checkpointing
        """
        X_train, Y_train = self.load_dataset(train_fn)
        X_dev, Y_dev = self.load_dataset(dev_fn)

        # Create a callback to print a sample after each epoch
        logging.debug("Training model on {}".format(train_fn))
        self.model.fit(X_train, Y_train,
                       batch_size = self.batch_size,
                       nb_epoch = self.epochs,
                       validation_data = (X_dev, Y_dev),
                       callbacks = self.get_callbacks(X_train))

    @staticmethod
    def load_dataset(fn, sep):
        """
        Load a supervised OIE dataset from file
        """
        return pd.read_csv(fn,
                           sep = sep,
                           header = None,
                           names = ['sent', 'base-pred', 'surface-pred'] + \
                           ['arg{}'.format(i) for i in range(10)],
                           engine = 'python'
        )

        # # Encode one-hot representation of the labels
        # if self.classes_() is None:
        #     self.encoder.fit(df.label.values)

        # # Split according to sentences and encode
        # sents = self.get_sents_from_df(df)
        # return (self.encode_inputs(sents),
        #         self.encode_outputs(sents))


if __name__ == "__main__":
    # Parse arguments
    args = docopt(__doc__)
    verbosity_level = logging.DEBUG if args['-v']\
                      else logging.INFO
    logging.basicConfig(level = verbosity_level)

    logging.debug(pformat(args))
    train_fn = args['--train']
    dev_fn = args['--dev']
    test_fn = args['--test']
    hyperparams_fn = args['--hyperparams']
    output_fn = args['--saveto']

    # Parse hyperparams and initialize model
    hyperparams = json.load(open(hyperparams_fn))['hyperparams']
    logging.debug("Model hyperparms: {}".format(pformat(hyperparams)))
    df = Seq2seq_OIE.load_dataset(train_fn, str(hyperparams['sep']))
#    s2s = Seq2seq_OIE(**hyperparams)
