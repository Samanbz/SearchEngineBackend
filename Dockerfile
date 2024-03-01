FROM python:3.10

ENV NEWS_API_KEY=be60a756bebf4fc3a62e64084f38b42e

ENV OPENAI_API_KEY=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

WORKDIR /server

copy ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host","0.0.0.0","--port","8000"]
