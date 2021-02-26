FROM acncio.azurecr.io/ubuntu20.04cio:latest

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
            r-base-dev \
		&& rm -rf /var/lib/apt/lists/*

# Remove Python 3.6.9 which comes as a part of common software bundle, due to vulnerability
#RUN apt-get purge -y python3
#RUN ls -l /usr/lib/python3.6
#RUN rm -rf /usr/lib/python3.6/*

# Dependencies for Python
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        zlib1g-dev \
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
        python3-distutils \
        # Needed for XML2, rjava & tidyverse
        libxml2-dev \
	&& rm -rf /var/lib/apt/lists/*

# Install Java
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        default-jre \
        default-jdk \
	&& rm -rf /var/lib/apt/lists/*

# Configure R with Java
RUN R CMD javareconf

# Set Working Directory
WORKDIR /app

#######################################
#####  gcloud Installation      #######
#######################################

# Installs google cloud sdk, this is mostly for using gsutil to export model.
RUN wget -nv \
    https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
    mkdir /app/tools && \
    tar xzf google-cloud-sdk.tar.gz -C /app/tools && \
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
RUN rm -rf /app/tools/google-cloud-sdk/platform/gsutil/third_party/httplib2/tests

#######################################
#####  copy files and scripts   #######
#######################################
COPY bootstrap_script.sh /app

# Install Required Packages
# R
RUN Rscript -e "install.packages(c('googleCloudStorageR','bigrquery','devtools','data.table'), quiet=TRUE, repos='https://cran.rstudio.com')"
# RUN Rscript -e "install.packages(c('devtools','Hmisc','rJava'), quiet=TRUE)"

# Install Packages for Python
RUN python3 -m pip install google-cloud-bigquery pandas pyarrow

WORKDIR /app
USER appuser:appgroup
ENTRYPOINT ["/microenforcer", "bash", "bootstrap_script.sh"]