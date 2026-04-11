# Testing Tika
```
curl -X PUT -T page-0291.jpg http://localhost:9998/rmeta/text -H "Accept: application/json" -H "X-Tika-OCRLanguage: deu"
```


# Local environment

## Ollama separate models
Start the required containers using docker compose.

```
docker compose up -d
```



Once the Ollama service is started, you can pull the required embedding model (nomic-embed-text) and 
generative model (llama3.2) in the ollama container:

For the embedder
```
docker compose exec ollama ollama pull nomic-embed-text
```

As answering LLM (optional)
```
docker compose exec ollama ollama pull llama3.2
```
## Ollama included Models

Build an image that includes the embedding model. No extra file storage needed
```
docker buildx build -t ollanma-embed -f DockerfileEmbedder .
```

## Call the embedding model via together.io

TODO