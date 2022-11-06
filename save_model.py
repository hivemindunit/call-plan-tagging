import sys
import nltk

from sentence_transformers import SentenceTransformer

def save_model(model_name: str):
    """Loads any model from Hugginface model hub and saves it to disk."""
    model = SentenceTransformer(model_name)
    model.save("./model")
    nltk.download('punkt', download_dir='./nltk_data')

if __name__ == "__main__":
    args = dict(enumerate(sys.argv))
    model_name = args.get(1, "all-mpnet-base-v2")
    save_model(model_name)