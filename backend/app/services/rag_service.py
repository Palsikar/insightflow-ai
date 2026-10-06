from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# Local embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Get embedding dimension
embedding_dimension = (
    embedding_model.get_sentence_embedding_dimension()
)


# Create FAISS vector index
index = faiss.IndexFlatL2(embedding_dimension)


# Store original documents
documents = []


def add_documents(texts):

    global index
    global documents

    # Clear existing vectors
    index.reset()

    # Clear existing documents
    documents.clear()

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True
    )

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    index.add(embeddings)

    documents.extend(texts)


def search_documents(query, top_k=3):

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx != -1 and idx < len(documents):
            results.append(documents[idx])

    return results


def create_profile_documents(profile):

    documents = []

    # Overall dataset information
    documents.append(
        f"""
Dataset overview:
Rows: {profile['rows']}
Columns: {profile['columns']}
Duplicate rows: {profile['duplicate_rows']}
"""
    )

    # Create one document for each column
    for column in profile["column_details"]:

        document = f"""
Column: {column['name']}
Data type: {column['data_type']}
Semantic type: {column['semantic_type']}
Missing values: {column['missing_values']}
Missing percentage: {column['missing_percentage']}
Unique values: {column['unique_values']}
Sample values: {column['sample_values']}
"""

        # Add numerical statistics if available
        if "statistics" in column:

            statistics = column["statistics"]

            document += f"""
Mean: {statistics['mean']}
Minimum: {statistics['minimum']}
Maximum: {statistics['maximum']}
Median: {statistics['median']}
Standard deviation: {statistics['standard_deviation']}
"""

        documents.append(document)

    return documents