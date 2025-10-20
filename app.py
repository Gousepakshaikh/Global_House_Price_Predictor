from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.constants import APP_HOST,APP_PORT
from typing import Optional
from src.pipeline.training_pipeline import TrainPipeline
from fastapi.responses import Response
from src.pipeline.prediction_pipeline import HouseData,HousePricePredictor



from uvicorn import run as app_run

app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")

templates=Jinja2Templates(directory="templates")
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class DataForm:
    def __init__(self,request:Request):
        self.request:Request=request
        self.Country:Optional[str]=None
        self.Property_Type:Optional[str]=None
        self.Furnishing_Status:Optional[str]=None
        self.Property_Size_SQFT:Optional[int]=None
        self.Previous_Owners:Optional[int]=None
        self.Rooms:Optional[int]=None
        self.Bathrooms:Optional[int]=None
        self.Garden:Optional[int]=None
        self.Monthly_Expenses:Optional[int]=None
        self.Neighbourhood_Rating:Optional[int]=None

    async def get_house_data(self):

        form=await self.request.form()
        self.Country=form.get("Country")
        self.Property_Type=form.get("Property_Type")
        self.Furnishing_Status=form.get("Furnishing_Status")
        self.Property_Size_SQFT=form.get("Property_Size_SQFT")
        self.Previous_Owners=form.get("Previous_Owners")
        self.Rooms=form.get("Rooms")
        self.Bathrooms=form.get("Bathrooms")
        self.Garden=form.get("Garden")
        self.Monthly_Expenses=form.get("Monthly_Expenses")
        self.Neighbourhood_Rating=form.get("Neighbourhood_Rating")

@app.get("/",tags=["authentication"])
async def index(request:Request):
    """
    Renders the main HTML form page for vehicle data input.
    """
    return templates.TemplateResponse(
        "House.html",{"request":request,"context":"Rendering"}
    )

@app.get("/train")
async def trainRouteClient():
    """
    Endpoint to initiate the model training pipeline.
    """

    try:
        train_pipeline=TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training Successful...")
    
    except Exception as e:
        return Response(f"Error Occurred! {e}")
    

@app.post("/")   
async def predictRouteClient(request:Request):
    """
    Endpoint to receive form data, process it, and make a prediction.
    """
    try:
        form=DataForm(request)
        await form.get_house_data()

        house_data=HouseData(
            country=form.Country,
            property_type=form.Property_Type, 
            furnishing_status=form.Furnishing_Status, 
            property_size_sqft=form.Property_Size_SQFT, 
            previous_owners=form.Previous_Owners, 
            rooms=form.Rooms, 
            bathrooms=form.Bathrooms,
            garden=form.Garden, 
            monthly_expenses=form.Monthly_Expenses,
            neighbourhood_rating=form.Neighbourhood_Rating    
        )
        
        house_df=house_data.get_house_input_data_frame()

        model_predictor=HousePricePredictor()

        value=model_predictor.predict(dataframe=house_df)[0]

        return templates.TemplateResponse("House.html",
            {"request": request, "context": value}
        )
        
    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)

