from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


# TF-IDF based lightweight retrieval
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

documents = []
document_vectors = None


def add_documents(texts):
    global documents
    global document_vectors

    documents = list(texts)

    if not documents:
        document_vectors = None
        return

    document_vectors = vectorizer.fit_transform(documents)


def search_documents(query, top_k=3):

    if not documents or document_vectors is None:
        return []

    query_vector = vectorizer.transform([query])

    scores = (
        document_vectors @ query_vector.T
    ).toarray().flatten()

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        if scores[index] > 0:
            results.append(documents[index])

    return results


def create_profile_documents(profile):

    profile_documents = []

    profile_documents.append(
        f"""
Dataset overview:
Rows: {profile['rows']}
Columns: {profile['columns']}
Duplicate rows: {profile['duplicate_rows']}
"""
    )

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

        if "statistics" in column:

            statistics = column["statistics"]

            document += f"""
Mean: {statistics['mean']}
Minimum: {statistics['minimum']}
Maximum: {statistics['maximum']}
Median: {statistics['median']}
Standard deviation: {statistics['standard_deviation']}
"""

        profile_documents.append(document)

    return profile_documents