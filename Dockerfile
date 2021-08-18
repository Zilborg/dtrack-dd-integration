FROM python:3.8.2-buster

# Copy sources
COPY . /service/server/

# Install pipenv
RUN apt update && apt install -y --no-install-recommends pipenv python3-psycopg2 \
    && \
	rm -rf /var/lib/apt/lists/* 

# Install app dependencies
WORKDIR /service/server
RUN pipenv install --deploy --system \
    && \
    rm -rf /root/.local/share/virtualenvs

# Clean tmp folder
RUN rm -rf /service/tmp/ \
   && \
   mkdir /service/tmp
