FROM python:3.4.5-slim

# make local directory and set it as default working dir
RUN mkdir /coinpl

WORKDIR /coinpl

# add local working directory into docker cwd
ADD . .

# dependencies
RUN pip install -r requirements.txt

# listening on port 5000
EXPOSE 5000

# run
CMD python manage.py runserver
