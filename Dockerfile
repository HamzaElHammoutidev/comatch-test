FROM python:3.7.6

# Install scripts dependencies
COPY . /comatch-test
ENV PYTHONPATH="${PYTHONPATH}:/comatch-test"
WORKDIR /comatch-test
RUN pip install -r /comatch-test/requirements.txt

# Docker-compose-wait tool
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# Start processes
ENTRYPOINT ["bash","script_wrapper.sh"]
