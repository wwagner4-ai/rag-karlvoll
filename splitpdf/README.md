
docker run -d -p 127.0.0.1:9998:9998 apache/tika:latest-full


curl -X PUT -T page-0291.jpg http://localhost:9998/rmeta/text -H "Accept: application/json" -H "X-Tika-OCRLanguage: deu"