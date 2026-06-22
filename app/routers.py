# this file handles the network calls
# uses the schema to validate the input
# orchestrate the processing
# format the output response

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.schemas import CallTranscriptRequest, AnalysisResponse
from app.services import AIService
from app.database import get_db
from app.models import IncidentLogTable


# industry standard versioning of APIs
router = APIRouter(prefix="/api/v1", tags=["Care Logistics"])

# declaring this endpoint will only listen to HTTP post network request
@router.post(
    "/analyze-log",
    response_model=AnalysisResponse, # FastAPI will drop the python dict returned by the 'analyze_call_log' function into the 'AnalysisResponse' schema, validate it and then serailize it JSON before sending it to the frontend.
    status_code=status.HTTP_201_CREATED, 
    summary="Process inbound call logs and parse structural attributes"
)
async def analyze_call_log(request: CallTranscriptRequest, db: Session = Depends(get_db)): # validates the incoming data and inputs data into the database

    # sending the validated transcript to the AI model
    # await -> non-blocking switch
    # when our system is busy computing a request
    # this thread will be paused so that application can process other incoming calls from the field workers
    # simultaneously
    structured_ai_data = await AIService.extract_structured_log(request.transcript)
    
    is_critical = structured_ai_data.get("severity") == "CRITICAL"


    # mapping the AI output parameters directly onto our database table fields
    db_record = IncidentLogTable(
        caller=structured_ai_data.get('caller'),
        patient_name=structured_ai_data.get('patient_name'),
        severity=structured_ai_data.get('severity'),
        requires_immediate_human_action=structured_ai_data.get('requires_immediate_human_action'),
        incident_summary=structured_ai_data.get('incident_summary'),
        raw_transcript=request.transcript
    )

    # add the table context and execute a permanent SQL insert commit onto disk
    db.add(db_record)
    db.commit()
    db.refresh(db_record) # brings the newly inserted object back into the memory so API can return it to frontend if needed
    
    # retuning a python dict. FastAPI will drop it on 'response_model=AnalysisResponse' filter to ensure data health and outputs a JSON response back to the frontend.
    return {
        "status": "Success",
        "data": structured_ai_data,
        "manager_alert_triggered": is_critical
    }
