FROM python:3.9-alpine
ADD caramell.py .
ADD requirements.txt .
RUN pip install -r requirements.txt

CMD ["python3", "caramell.py"]
