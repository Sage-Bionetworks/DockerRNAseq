# Use an official amazon linux image as the base
FROM amazonlinux:latest
MAINTAINER Ben Logsdon <ben.logsdon@sagebase.org>

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install package specific dependencies
RUN yum -y install wget gcc bzip2 ncurses-devel zlib-devel bzip2-devel xz-devel
RUN wget https://github.com/samtools/samtools/releases/download/1.6/samtools-1.6.tar.bz2
RUN tar -vxjf /app/samtools-1.6.tar.bz2
WORKDIR /app/samtools-1.6
RUN ./configure
RUN make
RUN make install

WORKDIR /app

RUN wget ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_24/gencode.v24.primary_assembly.annotation.gtf.gz
RUN gunzip gencode.v24.primary_assembly.annotation.gtf.gz
RUN ls

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

## Make port 80 available to the world outside this container
#EXPOSE 80

## Define environment variable
#ENV NAME World

# Run down_sample_re_count.py when the container launches
#CMD ["python", "down_sample_re_count.py","syn8569985","syn11587199"]
