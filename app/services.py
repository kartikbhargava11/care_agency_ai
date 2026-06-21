import httpx
import json
from fastapi import HTTPException
from config.settings import settings
from app.schemas import AnalyzedCallSchema

class AIService:
    @staticmethod
    async def extract_structured_log(transcript: str) -> dict:
        system_prompt = f"""
        [ROLE]
        You are a backend administrative parser for a home care agency. 
        Your sole function is to process inbound phone call transcripts and output raw JSON data.

        [TARGET SCHEMA]
        Populate your output data string to strictly match these JSON property types:
        {json.dumps(AnalyzedCallSchema.model_json_schema()['properties'], indent=2)}

        [CLASSIFICATION LOGIC]
        1. IDENTIFY THE CALLER TYPE:
        - "Field Worker": A staff member/carer reporting a shift status, client check, or an operational issue.
        - "Service User": A client/patient or their family member calling for an update, query, or care request.

        2. EVALUATE THE SEVERITY AND ACTION TRAFFIC:
        - Set 'severity' to 'CRITICAL' and 'requires_immediate_human_action' to true IF a Field Worker reports an emergency (e.g., client has fallen, client is aggressive, front door is locked/unresponsive) OR IF a Service User reports a missing worker or an acute safety issue.
        - Set 'severity' to 'ROUTINE' and 'requires_immediate_human_action' to false IF the text describes standard daily logs, shift scheduling updates, checkout notifications, or peaceful status updates.

        [OUTPUT CONSTRAINT]
        - Return ONLY the valid raw JSON object. 
        - Do not wrap in markdown tags like ```json ... ```. 
        - Do not generate notes, chatter, or conversational explanations.
        """
        
        payload = {
            "model": settings.AI_MODEL,
            "prompt": f"{system_prompt}\n\nInput Text:\n{transcript}",
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.0}
        }
        
        # Async HTTP client prevents blocking the execution loop of other incoming calls
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(settings.OLLAMA_URL, json=payload)
                response.raise_for_status()
                
                raw_response_text = response.json().get("response", "{}")
                return json.loads(raw_response_text)
                
            except httpx.HTTPError as err:
                raise HTTPException(status_code=502, detail=f"Ollama server connection fault: {err}")
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Local AI engine returned an unparseable response string.")
