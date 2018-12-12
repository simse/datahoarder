# Datahoarder
Hoarding data without the fuzz. Using this beautiful app you download massive quantities of public data for your local collection.

### Welcome to the beta
Datahoarder has no official release yet, however you are welcome to download and set up the beta. The beta should work at all times, but obviously problems could occur, so bear that in mind.

While in beta, the major version will be 0. So the very first beta release is 0.1.0.

### Installation
You are advised to use the Docker image like so:
```
docker pull simsemand/datahoarder
```
And then run:
```
docker run -p 4040:4040 -v CONFIG_PATH:/config ARCHIVE_PATH:/archive simsemand/datahoarder
```
Make sure to change `CONFIG_PATH` and `ARCHIVE_PATH` to where you want the configuration to be placed, and data to be downloaded, respectively.

### Usage
When the container is running, you can find the UI at `http://DOCKER_IP:4040/ui`. As it's your first time running, you'll get a welcome dialogue guiding you through setup. 

