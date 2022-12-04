A simple API asking for year of birth and posing follow-up questions depending on user age.

To run app:
```
pip install -r requirements.txt
uvicorn tuune_api:app --reload
```
To run tests:
```
pytest
```
Sample requests for interacting with API:

To begin
```
• curl localhost:8000
```

Age 35 and younger
```
• curl  -d '{"birth_year": 1990}' -H  "Accept: application/json"  -H "Content-Type: application/json" -X POST http://localhost:8000
```

Age over 35
```
• curl  -d '{"birth_year": 1980}' -H  "Accept: application/json"  -H "Content-Type: application/json" -X POST http://localhost:8000
```

Hair dye status
```
• curl  -d '{"dye_hair": true}' -H  "Accept: application/json"  -H "Content-Type: application/json" -X POST http://localhost:8000/hair_dye
```

Weight
```
• curl  -d '{"weight": 60}' -H  "Accept: application/json"  -H "Content-Type: application/json" -X POST http://localhost:8000/weight
```

To view submitted answers
```
• curl http://localhost:8000/answers
```
