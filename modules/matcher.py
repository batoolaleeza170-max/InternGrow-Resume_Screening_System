from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# AI Model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(resume_text, job_text):

    resume_embedding = model.encode(
        [resume_text]
    )

    job_embedding = model.encode(
        [job_text]
    )

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    score = round(float(similarity) * 100, 2)

    return score