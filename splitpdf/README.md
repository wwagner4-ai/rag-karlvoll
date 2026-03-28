Testing Tika
```
curl -X PUT -T page-0291.jpg http://localhost:9998/rmeta/text -H "Accept: application/json" -H "X-Tika-OCRLanguage: deu"
```

strt the required containers using docker compose.

```
docker compose up -d
```

Once the Ollama service is started, you can pull the required embedding model (nomic-embed-text) and 
generative model (llama3.2) in the ollama container:

```
docker compose exec ollama ollama pull nomic-embed-text
docker compose exec ollama ollama pull llama3.2
```

