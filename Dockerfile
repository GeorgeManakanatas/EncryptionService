FROM python:3.7.1-slim

RUN mkdir /home/docker_conda_template
WORKDIR /home/docker_conda_template

COPY . .

RUN apt-get update
RUN apt-get install -y --no-install-recommends
RUN apt-get install apt-utils gcc -y
RUN rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install cryptography
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
