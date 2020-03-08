FROM python:3.8
RUN git clone -b dev https://github.com/justmeandopensource/hello-banker-api /hello-banker-api
WORKDIR /hello-banker-api
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]