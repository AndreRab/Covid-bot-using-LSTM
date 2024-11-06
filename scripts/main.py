from application import Application
from model_manager import ModelManager
from model import EncoderDecoder

if __name__ == '__main__':     
    model = ModelManager()
    app = Application(model)
    app.start()