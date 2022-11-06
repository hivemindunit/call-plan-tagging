import json
from functools import lru_cache
from loguru import logger
import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from nltk import sent_tokenize
import nltk
nltk.data.path.append('./nltk_data')

@lru_cache
def get_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)

def endpoint(event, context):
    logger.info(event)
    try:
        request = json.loads(event["body"])
        questions = request.get("questions")
        assert questions, f"`questions` is required"
        transcript = request.get("transcript")
        assert transcript, f"`transcript` is required"

        sentences = sent_tokenize(transcript)
        model = get_model('model/')

        base_embeddings_sentences = model.encode(sentences, convert_to_tensor=True)
        base_embeddings = np.mean(np.array(base_embeddings_sentences), axis=0)

        vectors = []
        for i, document in enumerate(questions):
            # Encode question sentence vector
            sentences = sent_tokenize(document)
            embeddings_sentences = model.encode(sentences, convert_to_tensor=True)
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
        logger.info('=====================================')
        logger.info(highest_score)
        logger.info('T: ' + transcript)
        logger.info('Q: ' + questions[highest_score_index])

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
        logger.error(repr(e))

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