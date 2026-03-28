import splitpdf.helper as hlp_
import weaviate
from weaviate.classes.config import Configure
from weaviate.classes.config import Property, DataType
import json
from tqdm import tqdm


def embed_pages(clear_database: bool):

    texts = []
    files = list(hlp_.texts_dir().iterdir())
    files_sorted = sorted(files)
    for file in files_sorted:
        # print(file)
        text = json.loads(file.read_text())
        texts.append(text)

    with weaviate.connect_to_local() as client:
        if clear_database and client.collections.exists(hlp_.COLLECTION_NAME):
            print(f"Delete collection '{hlp_.COLLECTION_NAME}'")
            client.collections.delete(hlp_.COLLECTION_NAME)

        collection = client.collections.create(
            name=hlp_.COLLECTION_NAME,
            vector_config=Configure.Vectors.text2vec_ollama(  # Configure the Ollama embedding integration
                api_endpoint="http://ollama:11434",  # If using Docker you might need: http://host.docker.internal:11434
                model="nomic-embed-text",
            ),
            properties=[
                Property(
                    name="text",
                    vectorize_property_name=True,
                    data_type=DataType.TEXT,
                ),
                Property(
                    name="page_number",
                    vectorize_property_name=True,
                    data_type=DataType.INT,
                ),
            ],
        )

        print(
            f"Start embedding {len(texts)} objects to collection '{hlp_.COLLECTION_NAME}'"
        )
        collection = client.collections.use(hlp_.COLLECTION_NAME)
        with collection.batch.fixed_size(batch_size=1, concurrent_requests=1) as batch:
            for obj in tqdm(texts):
                batch.add_object(properties=obj)
                # print(f"## Added {obj['page_number']}")
