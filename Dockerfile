FROM python:alpine3.17
WORKDIR /app
COPY . .
RUN pip install flask
RUN pip install flask_restful
RUN pip install requests
ENV FLASK_APP="main.py"
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
EXPOSE 8000
CMD ["flask", "run", "--debug"]

# FROM python:alpine3.17
# WORKDIR /app
# COPY main.py .
# RUN pip install flask
# RUN pip install flask_restful
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_RUN_PORT=8000
# EXPOSE 8000
# CMD ["flask", "run", "--host=$FLASK_RUN_HOST", "--port=$FLASK_RUN_PORT"]
