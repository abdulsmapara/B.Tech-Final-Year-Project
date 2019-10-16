import random
from pathlib import Path
import spacy, textacy
import textacy.keyterms
import textacy.preprocessing
from spacy.util import minibatch, compounding

def custom_train_NER(model=None, TRAIN_DATA=None, model_file=None, no_iteration=100):
    '''
    Online training of pre-existing or newly created SpaCy NER Model
    Parameters:
        model        : Pre-defined spacy model (NER)
        model_dir    : Location to save the model after training
        no_iteration : Number of iteration in the training process
    '''

    '''Quick precheck whether training data is not null'''
    if TRAIN_DATA is None:
        print("Training data is empty! Abort!")
        return

    '''Loading model'''
    if model is None:
        ner_model = spacy.load('en')
    else:
        ner_model = spacy.load(model)

    '''Loading NER pipe of the model'''
    if "ner" not in ner_model.pipe_names:
        ner = ner_model.create_pipe("ner")
        ner_model.add(ner, last=True)

    else:
        ner = ner_model.get_pipe("ner")

    '''Adding new labels'''
    for _, annotations in TRAIN_DATA:
        for _,_,label in annotations['entities']:
            ner.add_label(label)

    other_pipes = [pipe for pipe in ner_model.pipe_names if pipe != "ner"]
    '''
    Disabling pipes other than NER
    Only NER model will be updated
    '''
    print("Training . . . ", end='')
    with ner_model.disable_pipes(*other_pipes):
        if not model:
            ner_model.begin_training()

        '''Iterated training'''
        for itr in range(no_iteration):
            random.shuffle(TRAIN_DATA)

            loss_function = {}
            '''Batch up the training data using SpaCy's minibatch'''
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))

            for batch in batches:
                sent, annotations = zip(*batch)
                '''
                Updating the model
                Parameters:
                    sent        : Sentences in the batch
                    annotations : List of entities and their location in the sentence
                    drop        : Dropout - make it harder to memorise data 
                '''
                ner_model.update(sent, annotations, drop=0.5, losses=loss_function,)

            # print("Losses", loss_function)

        '''End of training'''

    '''Saving the updated NER Model'''
    if model_file is not None:
        ner_model.to_disk(model_file)

    '''Everything complete'''
    print("Done")


def test_NER(fileinput, model=None, labels=[]):
    '''
    Testing of a SpaCy Model
    Parameters:
        model     : spacy model to be tested
        fileinput : Text file for testing (input)
    Returns:
        labeld entity along with sentence
    '''
    
    '''Loading model'''
    if model is None:
        ner_model = spacy.load('en')
    else:
        ner_model = spacy.load(model)

    '''Reading the content of the file'''
    file = textacy.io.read_text(fileinput, lines=True)
    content = ""

    '''Converting into SpaCy Doc'''
    for line in file:
        # line = textacy.preprocessing.remove_punctuation(line)
        docx = textacy.make_spacy_doc(line)
        content += str(docx)

    '''Passing the Doc to NER Model'''
    output = ner_model(content)

    '''Fetching the recognized entities and corresponding sentences and storing into dictionary'''
    ent_rec = {}
    for entity in output.ents:
        if len(labels) == 0:
            ent_rec[entity.text] = [entity.label_, entity.sent[:-1]]

        else:
            if str(entity.label_) in labels:
                ent_rec[entity.text] = [entity.label_, entity.sent[:-1]]

    '''Printing the output'''
    print("Output : \n")
    for key in ent_rec:
        print("{} : {} [{}]".format(key, ent_rec[key][0], ent_rec[key][1]))

    '''Returns the dictionary'''
    return ent_rec