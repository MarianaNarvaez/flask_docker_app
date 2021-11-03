FROM tiangolo/uwsgi-nginx:python3.6

ENV http_proxy http://naproxy.o-i.intra:8081
ENV https_proxy http://naproxy.o-i.intra:8081
ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 64
ENV NGINX_WORKER_PROCESSES auto
ENV NGINX_WORKER_CONNECTIONS 2048
ENV NGINX_WORKER_OPEN_FILES 2048

########################## SQL Driver for Linux configurations
RUN apt-get update

RUN apt-get install -y software-properties-common

RUN curl https://packages.microsoft.com/keys/microsoft.asc --insecure | apt-key add -

RUN curl https://packages.microsoft.com/config/debian/10/prod.list --insecure > /etc/apt/sources.list.d/mssql-release.list

RUN apt-add-repository https://packages.microsoft.com/debian/10/prod

RUN apt-get update

RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN ACCEPT_EULA=Y apt-get install -y mssql-tools

RUN apt-get install -y unixodbc-dev

RUN sed -i -E 's/(CipherString\s*=\s*DEFAULT@SECLEVEL=)2/\11/' /etc/ssl/openssl.cnf

########################## Flask specific configurations
ENV LISTEN_PORT 8080

EXPOSE 8080

ENV STATIC_URL /static

ENV STATIC_PATH /var/www/app/static

########################## Manning specific configurations

COPY ./requirements.txt /var/www/requirements.txt

RUN pip install -r /var/www/requirements.txt

COPY . . /var/www/app/

########################## RUN main command
#CMD ["python", "-i", "/var/www/app/Manning.py"]
CMD ["python", "/var/www/app/Manning.py"]
