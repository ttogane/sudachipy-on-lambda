FROM public.ecr.aws/lambda/python:3.8

ENV PROJECT_DIR="lambda"

# copy requirements.txt
COPY ./${PROJECT_DIR}/requirements.txt ./

# install gcc
RUN yum install -y gcc

# pip upgrade and install from requirments.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy app.py
COPY ./${PROJECT_DIR}/app.py ./

# handler
CMD ["app.handler"]