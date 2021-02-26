FROM acncio.azurecr.io/ubuntu18.04cio:latest

# LABEL name="non_standarad_package_check"
# LABEL version="20200905.1"
# LABEL maintainer="Model Management Team <cio.cap.advancedanalytics@accenture.com>"
# LABEL description="Non-Standard package check based on ubuntu 18.04 base standard image"
ARG APPDIR=/app

# Update and install gnupg2
RUN apt-get update && apt-get install -y gnupg2

# Update the key server
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9

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
		python3-dev \
	&& rm -rf /var/lib/apt/lists/*

# Install the package that is needed for the execution
RUN python3 --version \
	&& python3 -m pip --version

RUN python3 -m pip install --upgrade pip \
	&& python3 -m pip install setuptools --upgrade \
	&& python3 -m pip --version

# Copy Requirements.txt into working directory
WORKDIR ${APPDIR}
COPY requirements.txt ${APPDIR}

# Install Packages into Virtual Enviornment
RUN python3 -m pip install -r ${APPDIR}/requirements.txt \
        && python3 -m pip install -U pip-licenses

# Remove Vulnerabilties: For h2o
RUN rm -r /usr/local/lib/python3.6/dist-packages/future/backports/test

USER appuser:appgroup
# ENTRYPOINT ["/microenforcer"]
ENTRYPOINT ["/microenforcer", "pip-licenses"]
CMD ["--from=mixed"]