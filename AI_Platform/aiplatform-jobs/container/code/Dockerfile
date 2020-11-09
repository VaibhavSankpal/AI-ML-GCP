FROM acncio.azurecr.io/ubuntu18.04cio:latest

LABEL name="aqua_r_base"
LABEL version="20200608.1"
LABEL maintainer="JigarC <jigar.chhadwa@accenture.com>"
LABEL description="R based container image for AI Platform Jobs based on ubuntu 18.04 base standard image"

# Update and install gnupg2
RUN apt-get update && apt-get install -y gnupg2

# Update the key server
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9

# Install some useful tools and dependencies for MRO
RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
		software-properties-common \
		&& rm -rf /var/lib/apt/lists/*
	
# Add following entry to install latest R version - https://cloud.r-project.org/bin/linux/ubuntu/README.html
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/'

# Install latest R
RUN apt-get update \
		&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
			r-base \
		&& rm -rf /var/lib/apt/lists/*

# Remove Python 3.6.9 which comes as a part of common software bundle, due to vulnerability
#RUN apt-get purge -y python3
#RUN ls -l /usr/lib/python3.6
#RUN rm -rf /usr/lib/python3.6/*

# Dependencies for Python
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        zlib1g-dev \
        libncurses5-dev \
        libgdbm-dev \
        libnss3-dev \
        libssl-dev \
        libreadline-dev \
        libffi-dev \
        libsqlite3-dev \
		libcurl4-openssl-dev \
        wget \
        curl \
        ca-certificates \
		# Needed for Rcpp
		make \
		g++ \
        libblas-dev \
        liblapack-dev \
        # Needed for randomForest
        gfortran \
        python3-distutils \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

#######################################
#####  gcloud Installation      #######
#######################################

# Installs google cloud sdk, this is mostly for using gsutil to export model.
RUN wget -nv \
    https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
    mkdir /app/tools && \
    tar xvzf google-cloud-sdk.tar.gz -C /app/tools && \
    rm google-cloud-sdk.tar.gz && \
    /app/tools/google-cloud-sdk/install.sh --usage-reporting=false \
        --path-update=false --bash-completion=false \
        --disable-installation-options && \
    rm -rf /app/.config/* && \
    ln -s /app/.config /config && \
    # Remove the backup directory that gcloud creates
    rm -rf /app/tools/google-cloud-sdk/.install/.backup

# Path configuration
ENV PATH $PATH:/app/tools/google-cloud-sdk/bin
# Make sure gsutil will use the default service account
# RUN echo '[GoogleCompute]\nservice_account = default' > /etc/boto.cfg

# Upgrade pip to latest version
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py --force-reinstall && \
    rm get-pip.py

#######################################
#####  gcloud aqua fixes        #######
#######################################

# Remove the vulnerability identified by Aqua
RUN pip3 install httplib2 \
    && pip3 list -v \
    && rm -rf /app/tools/google-cloud-sdk/platform/gsutil/third_party/httplib2/python2/httplib2 \
    && cp -R /usr/local/lib/python3.6/dist-packages/httplib2 /app/tools/google-cloud-sdk/platform/gsutil/third_party/httplib2/python2/httplib2 \
    && rm -rf /app/tools/google-cloud-sdk/platform/gsutil/third_party/httplib2/python3/httplib2 \
    && cp -R /usr/local/lib/python3.6/dist-packages/httplib2 /app/tools/google-cloud-sdk/platform/gsutil/third_party/httplib2/python3/httplib2 \
    && gcloud --version

RUN pip3 install rsa \
    && pip3 list -v \    
    && rm -rf /app/tools/google-cloud-sdk/lib/third_party/rsa  \
    && cp -R /usr/local/lib/python3.6/dist-packages/rsa /app/tools/google-cloud-sdk/lib/third_party/rsa \
    && rm -rf /app/tools/google-cloud-sdk/platform/gsutil/third_party/rsa/rsa \
    && cp -R /usr/local/lib/python3.6/dist-packages/rsa /app/tools/google-cloud-sdk/platform/gsutil/third_party/rsa/rsa \
    && rm -rf /app/tools/google-cloud-sdk/platform/gsutil/third_party/httplib2/tests/tls/ca.key \
    && rm -rf /app/tools/google-cloud-sdk/platform/gsutil/third_party/httplib2/tests/tls/client.key \
    && rm -rf /app/tools/google-cloud-sdk/platform/gsutil/third_party/httplib2/tests/tls/client_encrypted.key \
    && rm -rf /app/tools/google-cloud-sdk/platform/gsutil/third_party/httplib2/tests/tls/server.key \
    && gcloud --version


#######################################
#####  copy files and scripts   #######
#######################################

COPY bootstrap_script.sh /app
RUN Rscript -e "install.packages(c('googleCloudStorageR','bigrquery'), quiet=TRUE)"

#RUN Rscript -e "install.packages(c('dplyr','doParallel','Boruta','mlbench','readr','caret'), quiet=FALSE)"

WORKDIR /app
USER appuser:appgroup
ENTRYPOINT ["/microenforcer", "bash", "bootstrap_script.sh"]