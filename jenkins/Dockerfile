FROM jenkins
USER root
RUN apt-get update && apt-get install -y python-dev python-pip libffi-dev libssl-dev rsync && pip install --upgrade cffi && pip install ansible && pip install virtualenv
USER jenkins
