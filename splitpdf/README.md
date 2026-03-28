
Starting Tika
```
docker run -d \
 --name tika \
 -p 127.0.0.1:9998:9998 \
 apache/tika:latest-full
```

Testing Tika
```
curl -X PUT -T page-0291.jpg http://localhost:9998/rmeta/text -H "Accept: application/json" -H "X-Tika-OCRLanguage: deu"
````

Starting Weaviate
````
 docker run -d \    
  --name weaviate \
  -p 8887:8080 \
  -p 50051:50051 \
  -v weaviate_data \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED='true' \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  cr.weaviate.io/semitechnologies/weaviate:1.24.1
```

