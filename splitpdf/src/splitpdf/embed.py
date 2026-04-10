import json
from dataclasses import dataclass

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.collections import Collection

import splitpdf.helper as hlp_


@dataclass
class Document:
    page_number: int
    text: str


class VectorDatabase:
    _client: weaviate.WeaviateClient | None = None

    def close(self) -> None:
        if self._client:
            self._client.close()

    def add_documents(
        self, collection_name: str, documents: list, clear_collection
    ) -> None:
        collection = self._get_collection(collection_name, do_clear=clear_collection)
        with collection.batch.fixed_size(batch_size=1, concurrent_requests=1) as batch:
            cnt = 0
            for obj in documents:
                print(f"---> embed obj {cnt} {obj['page_number']} {obj['text'][0:30]}")
                if cnt > 0 and cnt % 10 == 0:
                    print(f"Added {cnt} of {len(documents)} documents")
                batch.add_object(properties=obj)
                print(f"<--- embed obj {cnt} {obj['page_number']} {obj['text'][0:30]}")
                cnt += 1

    def query(self, collection_name: str, prompt: str) -> list[Document]:
        def to_document(doc: dict) -> Document:
            return Document(
                page_number=doc["page_number"],
                text=doc["text"],
            )

        coll = self._get_collection(collection_name)
        result = coll.query.hybrid(prompt, alpha=0.5, limit=5)
        return [to_document(obj.properties) for obj in result.objects]

    def _get_client(self) -> weaviate.WeaviateClient:
        if self._client is None:
            self._client = weaviate.connect_to_local()
        return self._client

    def _delete_collection(self, name: str) -> None:
        if self._get_client().collections.exists(name):
            self._get_client().collections.delete(name)

    def _create_collection(self, name: str) -> Collection:
        return self._get_client().collections.create(
            name=name,
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

    def _get_collection(self, name: str, do_clear: bool = False) -> Collection:
        client = self._get_client()
        if do_clear:
            self._delete_collection(name)
            return self._create_collection(name)
        if not client.collections.exists(name):
            return self._create_collection(name)
        return client.collections.use(name)


def query(prompt: str) -> None:
    database = VectorDatabase()
    try:
        collection_name = hlp_.COLLECTION_NAME
        documents = database.query(collection_name, prompt)
        if len(documents) == 0:
            print(f"Found no documents in {collection_name} for '{prompt}'")
        else:
            print(f"Found the following documents in {collection_name} for '{prompt}'")
            for i, doc in enumerate(documents):
                print(f"{i:4d} {doc.page_number:4d} - '{doc.text[:150]}...'")
    finally:
        database.close()


def embed_pages(clear_database: bool):
    texts = []
    files = list(hlp_.texts_dir().iterdir())
    files_sorted = sorted(files)
    for file in files_sorted:
        text = json.loads(file.read_text())
        texts.append(text)

    database = VectorDatabase()
    try:
        collection_name = hlp_.COLLECTION_NAME
        print(f"Start adding {len(texts)} documents to collection '{collection_name}'")
        database.add_documents(collection_name, texts, clear_database)
        print(f"Added {len(texts)} documents to collection '{collection_name}'")
    finally:
        database.close()
