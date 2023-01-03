import json
from cachetools import cached, LRUCache, TTLCache
import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from nltk import sent_tokenize
import nltk
nltk.data.path.append('./nltk_data')

@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)

model = get_model('model/')

@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def calculate_embeddings(document):
    tokenized_document = sent_tokenize(document)
    return model.encode(tokenized_document, convert_to_tensor=True)

def endpoint(event, context):
    try:
        request = json.loads(event["body"])
        questions = request.get("questions")
        assert questions, f"`questions` is required"
        transcript = request.get("transcript")
        assert transcript, f"`transcript` is required"

        base_embeddings_sentences = calculate_embeddings(transcript)
        base_embeddings = np.mean(np.array(base_embeddings_sentences), axis=0)

        vectors = []
        for i, document in enumerate(questions):
            # Encode question sentence vector
            embeddings_sentences = calculate_embeddings(document)
            embeddings = np.mean(np.array(embeddings_sentences), axis=0)
            vectors.append(embeddings)

        # Calculate cosine similarity between question and transcript vectors and return it
        scores = cos_sim(np.array(base_embeddings), np.array(vectors)).flatten()

        highest_score = 0
        highest_score_index = 0
        for i, score in enumerate(scores):
            if highest_score < score:
                highest_score = score
                highest_score_index = i

        response = {
            "index": highest_score_index,
            "score": highest_score.item()
        }

        # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-integration-settings-integration-response.html
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps(response),
        }
    except Exception as e:
        print(repr(e))

        # https://docs.aws.amazon.com/apigateway/latest/developerguide/handle-errors-in-lambda-integration.html
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"error": repr(e), "event": event, "context": context}),
        }

if __name__ == "__main__":
    print(endpoint({"body": json.dumps({"query": "vacation"})}, None)["body"])