# Covid-bot using LSTM neural network
![Pygame](https://img.shields.io/badge/Pygame-2.6.0-red)
![PyTorch](https://img.shields.io/badge/PyTorch-2.4.0-green)
![Torchvision](https://img.shields.io/badge/Torchvision-0.16.1-orange)
![NLTK](https://img.shields.io/badge/NLTK-3.7-blue)
![Issues](https://img.shields.io/github/issues/AndreRab/Spam-filter)

## The Covid-bot is designed to answer common questions about coronavirus.

### Description
In 2024, coronavirus isn't new, but we all remember how hard it was to find reliable information when the pandemic began. This inspired me to develop a chatbot using a Seq2Seq model with LSTM that can answer questions about this serious virus.

My project has two main components:
1. A **Pygame** application, where you can interact with the bot and ask questions.
2. A **Jupyter Notebook**, that documents the entire training process, with detailed comments.

Feel free to explore the project and ask the bot questions! Please note, however, that the bot is designed to answer only coronavirus-related questions.

## Table of Contents
| Section                      | Description                                                         |
|-------------------------------|---------------------------------------------------------------------|
| [Running the application](#running-the-application) | Instructions for running the Pygame application               |
| [Training process](#training-process)   | Information about the datasets used for training model and training process description      |
| [Jupyter Notebook](#jupyter-notebook)   | A detailed breakdown of the notebook |


## Running the application
0. **Install python interpreter** 
   How to make it, you can find [here](https://www.python.org/downloads/)
1. **Clone the Repository**:
   Open a terminal and clone the repository:
   ```bash
   git clone https://github.com/AndreRab/Spam-filter.git
   ```
2. **Navigate to the Project Directory**:
   Change your directory to the project folder:
    ```bash
    cd Spam-filter
    ```
3. **Install the necessary libraries**:
   Install the necessary libraries for properly application working:
   ```bash
   pip install -r requirements.txt
   ```
4. **Start the application**
   ```bash
   python scripts/main.py
   ```

## Training process
For training datasets, I used the following sources: [COVID19 frequent asked questions](https://www.kaggle.com/datasets/narendrageek/covid19-frequent-asked-questions) and [COVID19 related faqs](https://www.kaggle.com/datasets/deepann/covid19-related-faqs). In those datasets, there are only two columns: questions and answers. Therefore, I didn't need to perform any preprocessing before training my models. 

The LSTM model requires a long training time, which is why I trained it for over 300 epochs to achieve a satisfactory result. Naturally, the model doesn't perform perfectly for every question, as all embeddings were learned from scratch, and the dataset was not ideal.

## Jupyter Notebook
The [notebook](https://github.com/AndreRab/Covid-bot-using-LSTM/blob/main/research/Research.ipynb) is located in the **research** folder. There, you can see that I first created a vocabulary, where each word is assigned a unique ID. If a word is not in the vocabulary, it is assigned an unknown token.

Next, I defined the model, which is divided into two parts: an encoder and a decoder. Each part uses an LSTM block. For predictions, the model first encodes the question and then uses this encoding as input to the decoder. The decoder returns a probability distribution for each word in the vocabulary. I then use a grid-search approach to generate the answer.

You can also find a plot showing its learning process for first 100 epochs.
![image](https://github.com/user-attachments/assets/97345c1b-e6bb-4e20-a797-9d5e5bf736b9)


