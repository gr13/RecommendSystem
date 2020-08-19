FROM python:latest
RUN python3 -m ensurepip --upgrade
RUN pip3 install --upgrade pip

ENV STATIC URL /static
ENV STATIC_PATH /var/www/app/static

#EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this
# instruction creates a directory with this name if it doesn’t exist
WORKDIR /src

# install all python related packages
# specified in requirements.txt
COPY requirements.txt /src
RUN pip3 install -r requirements.txt
