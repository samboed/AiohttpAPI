FROM python:3.13.14-alpine

WORKDIR /aiohttp_api

RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["sh", "-c"]