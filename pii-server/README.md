# API endpoint for the PII server

How to run the server
* Install Poetry
* cd `cd pii-server/`
* Install dependicines with "poetry install"
* Run the server `poetry run uvicorn main:app --host 0.0.0.0 --port 8000`


Running with docker 

cd into the folder where docker-compose.yml file is
```
docker-compose up --build
```

```
docker-compose down
```


How to use the API
```
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, my name is Than Htut Soe, email is thanhtutsoetgi@gmail.com!"}' \
  http://localhost:8000/process
```
Response
```
{"redacted_text":"Hello, my name is [NAME], email is [EMAIL]!","status":"success"}
```

To get the history records in JSON
```
curl -X GET http://localhost:8000/history
curl -X GET http://localhost:8000/history?skip=100&limit=50 
```

