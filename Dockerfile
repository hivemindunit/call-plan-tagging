FROM public.ecr.aws/lambda/python:3.9

# Copy model directory into /var/task
ADD ./model ${LAMBDA_TASK_ROOT}/model/

# Copy model directory into /var/task
ADD ./nltk_data ${LAMBDA_TASK_ROOT}/nltk_data/

# Copy `requirements.txt` into /var/task
COPY ./requirements.txt ${LAMBDA_TASK_ROOT}/

# install dependencies
RUN python3 -m pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

# Copy function code into /var/task
COPY handler.py ${LAMBDA_TASK_ROOT}/

# Set the CMD to our handler
CMD [ "handler.endpoint" ]