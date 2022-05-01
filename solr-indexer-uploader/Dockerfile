FROM python:3.7-slim

WORKDIR /app

RUN pip3 install nltk pysolr requests unidecode uvicorn fastapi aiofiles python-multipart pdfplumber
COPY install_dictionary.py /install_dictionary.py
RUN python3 /install_dictionary.py
EXPOSE 8094

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8094"]