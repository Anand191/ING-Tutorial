#Base Image
FROM ubuntu:16.04

MAINTAINER Anand Singh <anand.singh@student.uva.nl>



########BEGIN INSTALLATION############
# System packages
RUN apt-get update && apt-get install -y curl
RUN apt-get install -y libssl-dev
RUN apt-get install -y build-essential
RUN apt-get install -y gcc
RUN apt-get install -y swig
RUN apt-get install -y libglib2.0-0
RUN apt-get -y install libgl1-mesa-glx

# Install miniconda to /miniconda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

###########END INTALLATION############

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

###########INSTALL APP DEPENDENCIES#########
#Install the breakout detection package
#RUN cd BreakoutDetection/Python
RUN swig -python -c++ breakout_detection.i
RUN /miniconda/bin/python setup.py build_ext -I./src build 
RUN /miniconda/bin/python setup.py build_ext -I./src install

# Python packages from conda
RUN conda install --yes --file requirements.txt
############END INSTALLATION################



# Expose the default port
EXPOSE 80

#Define Entrypoint
ENTRYPOINT ["/miniconda/bin/python", "ECP_test.py"]
#CMD ["python", "ECP_test.py"]

