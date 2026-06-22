FROM python:3.10-slim
# 'slim' python image
# faster download and cheap cloud storage fees

ENV PYTHONDONTWRITEBYTECODE=1 
# Instructs python never to write .pyc cache file to the container disk space
# keep the runtime environment clean and lightweight

ENV PYTHONUNBUFFERED=1
# forces python logs to steam instantly to the console terminal screen

WORKDIR /app
# creates a dedicated application folder inside the isolated linux environment
# auto changes our current terminal execution path directly into it

COPY ./requirements.txt /app/requirements.txt
# copy only the requirements.txt into the virual machine first
# critical optimization tactic
# dependencies change rarely

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# install the dependencies
# --no-cache-dir ->  prevents pip from caching downloaded files inside the container, saves disk space
# --upgrade -> ensures our package tool itself is running on the latest secure patch

COPY . /app/
# copy the rest of the local directories into the container
# optimization tactic to complete cloud builds in under 2 seconds

EXPOSE 8000
# informs the host cloud platforms that is container app is listening for incoming network data packets
# on port 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# runtime execution command that boots up the server
# main:app -> look inside main.py for the app = FastAPI() web instance
# --host 0.0.0.0 -> instructs the app to listen to external traffic coming from the public internet
# --port 8000 -> Bind the ASGI app server to port 8000

