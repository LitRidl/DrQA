from pymystem3 import Mystem
import copy
from .tokenizer import Tokens, Tokenizer


class RussianTokenizer(Tokenizer):

    def __init__(self, **kwargs):
        self.annotators = copy.deepcopy(kwargs.get('annotators', set()))
        self.tokenizer = Mystem()
        
    def tokenize(self, text):
        ner_names = set(['имя', 'гео', 'отч', 'фам'])
        clean_text = text.replace('\n', ' ')
        
        tokens = self.tokenizer.analyze(clean_text)

        data = []
        current_position_in_text = 0
        for i in range(len(tokens)):
            ner = ''
            tag = ''
            if tokens[i]['text'] == ' ' or tokens[i]['text'] == '\n':
                continue
            elif len(tokens[i]) >= 2:
                if len(tokens[i]['analysis']) < 1:
                    ner = 'ENG'
                    tag = tokens[i]['text']
                    lem = tokens[i]['text']
                else:
                    if self.annotators & {'pos'}:
                        description = tokens[i]['analysis'][0]['gr']
                        desc_ind = description.find('=')
                        tag = description[0:desc_ind]
                        parts_of_speech = tag.split(',')
                        tag = parts_of_speech[0]
                    if self.annotators & {'ner'}:
                        set_of_ner = set(parts_of_speech) & ner_names
                        if bool(set_of_ner):
                            ner = next(iter(set_of_ner))
                    lem = tokens[i]['analysis'][0]['lex']
            elif len(tokens[i]) < 2:
                tag = tokens[i]['text']
                lem = tokens[i]['text']
            data_text = tokens[i]['text']
            start = current_position_in_text
            end = current_position_in_text + len(data_text)
            if i + 1 < len(tokens):
                if tokens[i+1]['text'] != ' ' and tokens[i+1]['text'] != '\n':
                    text_in_text = text[start:end]
                    current_position_in_text += len(data_text)
                else:
                    text_in_text = text[start:end+1]
                    current_position_in_text += len(data_text) + 1
            else:
                text_in_text = text[start:end]
            indexes = (start, end)
            
            data.append((
                data_text,
                text_in_text,
                indexes,
                tag,
                lem,
                ner
            ))
            
        return Tokens(data, self.annotators, opts={'non_ent': ''})