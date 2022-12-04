from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

#Data models for user answers
class BirthYear(BaseModel):
    birth_year: int

class HairDye(BaseModel):
    dye_hair: bool

class Weight(BaseModel):
    weight: int
    

#Dictionary to store user answers in-memory    
user_data = {"What year were you born?": None, "Do you dye your hair?": None, "How much do you weigh (in kg)?": None}

#Returns error messages in plaintext for user convenience
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

#Custom error checking for appropriate birth year range
class BirthyearException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(BirthyearException)
async def birthyear_exception_handler(request: Request, exc: BirthyearException):
    return JSONResponse(
        status_code=418,
        content={"message": "The integer you have entered is outside of the possible range"},
    )

#Custom error checking for weight integers
class WeightException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(WeightException)
async def weight_exception_handler(request: Request, exc: WeightException):
    return JSONResponse(
        status_code=418,
        content={"message": "The integer you have entered cannot be negative"},
    )


#Ask user for birth year
@app.get("/")
async def ask_question_one():
    return JSONResponse(
        status_code=200,
        content={"Question one": "What year were you born? Please provide your answer as a JSON in the format {\'birth_year\': YOUR_ANSWER} through a POST API request to http://localhost:8000/, where the value of your answer is an integer"}
    )

#Record birth year and ask user for weight or about hair dyeing based on birth year
@app.post("/")
def ask_question_two(year: BirthYear):
    year_dict = year.dict()
    user_birth_year = year_dict["birth_year"]
    if user_birth_year < 0 or user_birth_year > 2022:
        raise BirthyearException(name="BirthyearException")
    else:
        user_data["What year were you born?"] = user_birth_year
        questions = {True:  {"Question two": "How much do you weigh (in kg)? Please provide your answer as a JSON in the format {\'weight\': YOUR_ANSWER} through a POST API request to http://localhost:8000/weight, where the value of your answer is an integer"}, False: {"Question two": "Do you dye your hair? Please provide your answer as a JSON in the format {\'hair_dye\': YOUR_ANSWER} through a POST API request to http://localhost:8000/hair_dye, where the value of your answer is an boolean"}}
        question_two = questions[user_birth_year < 1987]
        return JSONResponse(
        status_code=200,
        content=question_two
    )

#Record whether user dyes hair
@app.post("/hair_dye")
async def question_two_hairdye(dye: HairDye):
    hair_dict = dye.dict()
    user_hair_dye = hair_dict["dye_hair"]
    user_data["Do you dye your hair?"] = user_hair_dye
    return JSONResponse(
        status_code=200,
        content={"Message": "Your answers have been received. You can view them through a GET API request to localhost:8000/answers"}
    )
    
#Record user weight
@app.post("/weight")
async def question_two_weight(weight: Weight):
    weight_dict = weight.dict()
    user_weight = weight_dict["weight"]
    if user_weight < 0:
        raise WeightException(name="WeightException")
    else:
        user_data["How much do you weigh (in kg)?"] = user_weight
        return JSONResponse(
        status_code=200,
        content={"Message": "Your answers have been received. You can view them through a GET API request to localhost:8000/answers"}
    )

#Returns record of user answers
@app.get("/answers")
async def return_answers():
    return JSONResponse(
        status_code=200,
        content={"User data": user_data}
    )







