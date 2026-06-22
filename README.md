# AI Coordinator for Care Agencies
For a door-to-door agency, the biggest cost leak is 'administrative lag' (support workers wasting hours typing notes instead of providing care, or critical emergencies getting buried in an inbox).

## How this system cut costs and generates revenue
### 1. Slashes operational overheads
A standard care agency requires 3 to 4 full-time coordinators sitting at desks just to answer phones, type up handwritten logs, and call carers who are late. By automating routine logs, one coordinator can manage 4x more field workers, instantly multiplying profit margins.

### 2. Ensures 100% perfect and timestamped notes
In healthcare and care agencies, clean note-keeping is legally required for government funding or private insurance payouts. If an incident happens and you don't have an audit trail, you get fined. This AI ensures 100% perfect, timestamped records for every single visit automatically, protecting your revenue.

### 3. 24/7 Active
If a prospective client calls your number off an ad at 2:00 AM, the AI answers instantly, qualifies their budget, extracts their needs, logs them into the CRM as a "Warm Lead," and texts them a calendar link to book a consultation with you the next morning. You capture leads your competitors miss because their offices are closed.



## Local Installation

### 1. Build and run a multi-container System
Ensure Docker Desktop is open and active on the machine. From your project root, execute:

```sh
docker compose up --build
```

### 2. Inject the Local Model Brain (Run Only Once)
Since the containerized Ollama engine boots up completely blank, run this command in a separate terminal tab to download and lock the parameter weights permanently onto your local disk storage

```bash
docker exec -it coordinator_bonnie ollama run qwen2.5:1.5b
```



