# Deprecated! 
The maintenance of this project has moved to the [AllenNLP framework](https://allennlp.org/). <br>
Where you can use [the model and an online demo](http://demo.allennlp.org/open-information-extraction).
This [thin wrapper](https://github.com/gabrielStanovsky/supervised_oie_wrapper) may also be useful if you want to run the pretrained model.


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [supervised-oie](#supervised-oie)
  - [Citing :bookmark:](#citing-bookmark)
  - [Quickstart :hatching_chick:](#quickstart-hatching_chick)
  - [More scripts :bicyclist:](#more-scripts-bicyclist)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# supervised-oie
Code for training a supervised Neural Open IE model, as described in our [NAACL2018 paper](https://gabrielstanovsky.github.io/assets/papers/naacl18long/paper.pdf).<br>
:construction: *Still under construction* :construction:


Citing :bookmark:
------
If you use this software, please cite:
```
@InProceedings{Stanovsky2018NAACL,
  author    = {Gabriel Stanovsky and Julian Michael and Luke Zettlemoyer and Ido Dagan},
  title     = {Supervised Open Information Extraction},
  booktitle = {Proceedings of The 16th Annual Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL HLT)},
  month     = {June},
  year      = {2018},
  address   = {New Orleans, Louisiana},
  publisher = {Association for Computational Linguistics},
  pages     = {(to appear)},
}
```

Quickstart :hatching_chick:
-----------

1. Install requirements :bow:
```bash
pip install requirements.txt
```

2. Download embeddings :walking:
```bash
cd ./pretrained_word_embeddings/
./download_external.sh
```

3. Train model :running:
```bash
cd ./src
python  ./rnn/confidence_model.py  --train=../data/train.conll  --dev=../data/dev.conll  --test=../data/test.conll --load_hyperparams=../hyerparams/confidence.json```
```
***NOTE:*** Models are saved by default to the models dir, unless a "--saveto"
command line argument is passed. See [confidence_model.py](src/rnn/confidence_model.py) for more details. 

4. Predict with a trained model :clap:
```bash
python ./trained_oie_extractor.py \
    --model=path/to/model \
    --in=path/to/raw/sentences
    --out=path/to/output/file
    --conll
```

More scripts :bicyclist:
------------

See [src/scripts](src/scripts) for more handy scripts. Additional documentation coming soon!

