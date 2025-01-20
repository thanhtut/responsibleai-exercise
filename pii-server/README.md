# API endpoint for the PII server

How to run the server
* Install Poetry
* cd `cd pii-server/`
* Install dependicines with "poetry install"
* Run the server `uvicorn main:app --host 0.0.0.0 --port 8000`


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