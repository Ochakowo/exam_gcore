FROM python:3.12-alpine

WORKDIR /ui_test_app

COPY requirements.txt pytest.ini ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["pytest"]
