FROM acncio.azurecr.io/ubuntu18.04cio:latest

LABEL name="nltk_package_check"
LABEL version="20200905.1"
LABEL maintainer="Model Management Team <cio.cap.advancedanalytics@accenture.com>"
LABEL description="NLTK package check based on ubuntu 20.04 base standard image"
ARG APPDIR=/app

# Update and install gnupg2
RUN apt-get update && apt-get install -y gnupg2

# Update the key server
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9

# Install some useful tools and dependencies for MRO
RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		software-properties-common \
		&& rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        python3-distutils \
		python3-pip \
		python3-setuptools \
	&& rm -rf /var/lib/apt/lists/*

# Install the package that is needed for the execution
RUN python3 --version \
	&& python3 -m pip --version

# Install Packages into Virtual Enviornment
RUN python3 -m pip install -U pip-licenses

# Download and install NLTK
RUN pip3 install -U nltk
RUN python3 -m nltk.downloader -d ./ "#{nltkdataname}#"

USER appuser:appgroup
#ENTRYPOINT ["/microenforcer"]
ENTRYPOINT ["/microenforcer", "pip-licenses"]
CMD ["--from=mixed"]