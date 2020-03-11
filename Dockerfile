FROM python:3.8
WORKDIR /hello-banker-api
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]