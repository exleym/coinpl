FROM python:3.4.5-slim

# make local directory and set it as default working dir
RUN mkdir /coinpl

WORKDIR /coinpl

# add local working directory into docker cwd
ADD . .

# dependencies
RUN pip install -r requirements.txt

# listening on port 8000
EXPOSE 8000

# run
CMD gunicorn run:app -b :8000 --name app --log-level=debug --log-file=-
