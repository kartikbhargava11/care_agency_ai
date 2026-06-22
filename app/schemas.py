# this file handles data validation
# making sure no bad or malformed data enters in and sent out
# The Internet (Incoming JSON) -> Pydantic Schema (Data Control) -> FastAPI and Logic (Route Controller)

from pydantic import BaseModel, Field # BaseModel is a class from pydantic library. it turns a standard python class into a fast data validator

from typing import Literal

# handles incoming raw data into the app from the frontend
# pydantic intercepts the incoming data if incoming data doesn't contain 'transcript' 
# or the string is shorter than 10 characters, the request will be blocked
class CallTranscriptRequest(BaseModel):
    # ... -> Ellipsis literal
    # a mathematical command to the framework
    # it says, the data is required. 
    transcript: str = Field(..., min_length=10, description="Raw audio transcript text from the phone line.")

# following class defines the internal database structure that we want our AI model to extract from the raw transcript
class AnalyzedCallSchema(BaseModel):
    caller: str = Field(..., description="The name of the individual who placed the call.")
    patient_name: str = Field(..., description="The name of the target client/patient discussed.")
    severity: Literal["CRITICAL", "ROUTINE"] = Field(..., description="The classification priority metric.")
    requires_immediate_human_action: bool = Field(..., description="True if manual operational override is urgent.")
    incident_summary: str = Field(..., description="A 1-sentence clean operational digest summary.")

# it handles data going out of the app back to the frontend
# instead of returning raw, unformatted data, it forces the API to output a structured layout
class AnalysisResponse(BaseModel):
    status: str = "Success"
    data: AnalyzedCallSchema
    manager_alert_triggered: bool
