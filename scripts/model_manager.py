import json
import os
import torch # type: ignore
import string
from model import EncoderDecoder

import nltk  # type: ignore
from nltk.tokenize import word_tokenize  # type: ignore


class ModelManager():
    def __init__(self) -> None:
        self.load_vocabular()
        self.load_model()
        self.model.load(self.word2ind, self.ind2word)

    def load_vocabular(self):
        self.word2ind = {}
        self.ind2word = {}
        with open('json_data/word2ind.json', 'r') as f:
            self.word2ind = json.load(f)
            print('Word 2 index was loaded')

        with open('json_data/ind2word.json', 'r') as f:
            self.ind2word = json.load(f)
            print('Index 2 word was loaded')

        self.word2ind = {key: int(value) for (key, value) in self.word2ind.items()}
        self.ind2word = {int(key): value for (key, value) in self.ind2word.items()}

    def load_model(self):
        self.model = EncoderDecoder(16848, 256, 64, max_answer_length=128, teaching_forcing=0.8) 
        if os.path.exists('model/model_weights.pth'):
            self.model.load_state_dict(torch.load('model/model_weights.pth', weights_only=True))
            print("Model was loaded")
        else:
            print("Model wasn't found")
        self.model.eval()

    def generate_response(self, str):
        tokenized_sentence = self.string_preproc(str)
        tokenized_sentence = tokenized_sentence.unsqueeze(0) 
        with torch.no_grad():
            probs_tensor = self.model(tokenized_sentence)
            indexes = probs_tensor.argmax(axis=-1).reshape(-1)
            output = [self.ind2word[index.item()] + " " for index in indexes]

            if '<eos>' + " " in output:
                output = output[:output.index('<eos>' + " ") + 1]

            reresponse = self.data_postproc(''.join(output))
            return reresponse
        
    def data_postproc(self, text):
        signs = '\'()[].,?!:; '
        result = ""
        is_newSentence = True

        words = text.split(" ")
        for word in words:
            if word == '<bos>' or word == '<eos>':
                pass
            elif word == '<unk>':
                result += 'COVID19' + " "
            elif word in signs:
                result = result[:-1]
                result += word + " "
                if word == '.':
                    is_newSentence = True
            elif is_newSentence:
                result += word[0].upper() + word[1:] + " "
                is_newSentence = False
            else:
                result += word + " "

        return result
    
    def string_preproc(self, str, max_len = 256):
        processed_text = str.lower().translate(
            str.maketrans("", "", string.punctuation))
        tokenized_sentence = [self.word2ind['<bos>']]
        tokenized_sentence += [self.word2ind.get(word, self.word2ind['<unk>'])
                               for word in word_tokenize(processed_text)]
        tokenized_sentence += [self.word2ind['<eos>']]
        for _ in range(max_len - len(tokenized_sentence)):
            tokenized_sentence.append(self.word2ind['<pad>'])

        return torch.LongTensor(tokenized_sentence)
