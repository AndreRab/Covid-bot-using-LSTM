import torch.nn as nn # type: ignore
import torch # type: ignore
import random

class EncoderDecoder(nn.Module):
    def __init__(self, vocab_len, hidden_dim, input_size, max_answer_length, teaching_forcing=1.0):
        super(EncoderDecoder, self).__init__()
        self.vocab_len = vocab_len
        self.hidden_dim = hidden_dim
        self.input_size = input_size
        self.teaching_forcing = teaching_forcing
        self.max_answer_length = max_answer_length
        self.word2ind = {}
        self.ind2word = {}

        self.encoder_embedding = nn.Embedding(vocab_len, input_size, padding_idx=self.word2ind.get('<pad>', 0))
        self.encoder_LSTM = nn.LSTM(
            input_size=self.input_size,
            hidden_size=self.hidden_dim,
            num_layers=2,
            batch_first=True,
            dropout=0.2
        )

        self.decoder_embedding = nn.Embedding(vocab_len, hidden_dim, padding_idx=self.word2ind.get('<pad>', 0))
        self.decoder_LSTM = nn.LSTM(
            input_size=self.hidden_dim,
            hidden_size=self.hidden_dim,
            num_layers=2,
            batch_first=True,
            dropout=0.2
        )

        self.decoder_prediction = nn.Sequential(
            nn.Linear(hidden_dim, vocab_len)
        )
    
    def load(self, word2ind, ind2word):
        self.word2ind = word2ind
        self.ind2word = ind2word

    def forward(self, x, target = None, device='cpu'):
        batch_size = x.shape[0]

        # Encoder
        embeddings = self.encoder_embedding(x)
        output, hidden = self.encoder_LSTM(embeddings)

        # Previous tokens for batch
        prev_token_idx = torch.tensor([self.word2ind['<bos>']] * batch_size).reshape(-1, 1).to(device)

        probs_tensor = None
        for i in range(self.max_answer_length):
            if i != 0 and target is not None and random.random() < self.teaching_forcing and target.shape[1] > i - 1:
                prev_token_idx = target[:, i - 1].reshape(-1, 1).to(device)
            embeddings = self.decoder_embedding(prev_token_idx)
            output, hidden = self.decoder_LSTM(embeddings, hidden)

            # Output is distribution for prediction
            output = self.decoder_prediction(output)
            # New previous token
            prev_token_idx = output.argmax(axis=2).reshape(-1, 1)  # axis=2 for batch-first

            if probs_tensor is None:
                probs_tensor = output.unsqueeze(0)
            else:
                probs_tensor = torch.cat((probs_tensor, output.unsqueeze(0)))

            if target is not None and i == target.shape[1] - 1:
                break

        # Transpose for dimension swapping
        return probs_tensor.transpose(1, 0)