import ast
import astrapy
import numpy as np
import os
import pandas as pd
import uuid

from tqdm import tqdm


def vector_str_manipulation(vector_str):
    # Function to convert vector string to list of floats
    while '  ' in vector_str:
        vector_str = vector_str.replace('  ', ' ')

    vector_str = vector_str.replace(' ', ',')

    while ',,' in vector_str:
        vector_str = vector_str.replace(',,', ',')

    return vector_str.replace('[,', '[').replace(',]', ']')


def convert_vector(vector_str):
    # print(f'{vector_str=}')
    vector_str = vector_str_manipulation(vector_str)

    if isinstance(vector_str, str):
        return [float(x) for x in ast.literal_eval(vector_str)]
    elif isinstance(vector_str, float):
        return [vector_str]
    elif isinstance(vector_str, np.array):
        return list(vector_str)
    else:
        print(f'{type(vector_str)=}')
        return vector_str


# Function to generate documents from CSV rows


def generate_document(row):
    return {
        "_id": row["uuid"] if "uuid" in row else str(uuid.uuid4()),
        "qid": row["qid"],
        "pid": row["pid"],
        "value": row["value"],
        "item_label": row["item_label"],
        "property_label": row["property_label"],
        "value_content": row["value_content"],
        "statement": row["statement"],
        # Convert string to vector
        "embedding": convert_vector(row["embedding"])
    }

# Batch insert documents into the collection


def batch_insert_documents(collection, documents, label=''):
    try:
        collection.insert_many(
            documents,
            vectors=[doc["embedding"] for doc in documents]
        )
    except Exception as err:
        # TODO: introduce recursive looking
        # batch_insert_documents(collection, documents, label=label)
        print(f'Error on Chunk {label}')
        print(f'Error: {err}')
        uuid_err_counter = 0
        with open('deletme', 'a', newline='\n') as fdel:
            for doc in tqdm(documents):
                try:
                    # Assign new UUID
                    # doc["_id"] = str(uuid.uuid4())
                    collection.insert_one(
                        doc,
                        vector=doc["embedding"]
                    )
                except Exception as err2:
                    uuid_err = "Failed to insert document with _id"
                    # uuid_err = "Document already exists with the given _id"

                    if uuid_err not in str(err2):
                        print(f'Inner error: {err2}')
                    else:
                        uuid_err_counter = uuid_err_counter + 1

                    fdel.write(f'{doc["embedding"]},{err},{err2}\n')

            print(f'Number of UUID already exists errors: {uuid_err_counter}')


# Read CSV in chunks and upload to Astra DB


def upload_csv_to_astra(csv_file=None, df=None, ch_size=100):

    if csv_file is not None and df is None:
        iterator = enumerate(pd.read_csv(csv_file, chunksize=ch_size))
        for k, chunk in tqdm(iterator):
            documents = [
                generate_document(row) for index, row in chunk.iterrows()
            ]
            batch_insert_documents(collection, documents, label=k)
    elif df is not None:
        iterator = enumerate(pd.read_csv(csv_file, chunksize=ch_size))
        for k, row in tqdm(df.iterrows()):
            documents = [generate_document(row)]
            batch_insert_documents(collection, documents, label=k)


# Initialize the DataStax Astra client

api_url_id = ''

api_url = os.environ.get('ASTRACS_API_URL')
app_token = os.environ.get('ASTRACS_API_KEY')

client = astrapy.DataAPIClient(app_token)
database = client.get_database_by_api_endpoint(api_url)
collection = database.get_collection("testwikidata")

# Path to the CSV file
csv_file_path = './csvfiles/wikidata_vectordb_datadump_10000_en.csv'

# print(f'Loading {csv_file_path}')
# df = pd.read_csv(csv_file_path)

# Clear deleteme file
with open('deletme', 'w', newline='\n') as fdel:
    fdel.write('')

# Upload the CSV data to Astra DB
upload_csv_to_astra(df=None, csv_file=csv_file_path, ch_size=100)
