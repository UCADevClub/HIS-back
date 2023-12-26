# pull official base image
FROM python:3.11.3-alpine

# set work directory
WORKDIR ./HIS-back

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
#COPY ./entrypoint.sh .
#RUN sed -i 's/\r$//g' /D:/work/DevClub/HIS-Project/HIS-back/entrypoint.sh
#RUN chmod +x /D:/work/DevClub/HIS-Project/HIS-back/entrypoint.sh
#
## copy project
#COPY . .
#
## run entrypoint.sh
#ENTRYPOINT ["/D:/work/DevClub/HIS-Project/HIS-back/entrypoint.sh"]
#
## copy project
COPY . .