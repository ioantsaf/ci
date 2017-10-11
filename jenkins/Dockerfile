FROM jenkins/jenkins:lts
USER root
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y python-dev python-pip libffi-dev libssl-dev rsync google-chrome-stable
RUN pip install --upgrade cffi && pip install ansible && pip install virtualenv
USER jenkins
