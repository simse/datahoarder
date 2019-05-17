<p align="center">
  <img alt="Datahoarder" src="https://i.imgur.com/xDm16RT.png" width="100" />
</p>
<h1 align="center">
  Datahoarder
</h1>
<p>
Datahoarder is a Python app for hoarding data.
</p>

# About
Datahoarder is a project that allows you to download massive amounts of data from various sources, while stayig up to date. Within the app, you'll find many different sources to hoard everything from Linux Distros to Creative Commons sound effects, whatever floats your boat!

# THIS IS A BETA

# Installation
You are advised to use the Docker image like so:
```
docker pull simsemand/datahoarder
```
And then run:
```
docker run -p 4040:4040 -v CONFIG_PATH:/config -v ARCHIVE_PATH:/archive simsemand/datahoarder
```
Make sure to change `CONFIG_PATH` and `ARCHIVE_PATH` to where you want the configuration to be placed, and data to be downloaded, respectively.

# Usage
When the container is running, you can find the UI at `http://DOCKER_IP:4040/ui`. As it's your first time running, you'll get a welcome dialogue guiding you through setup. 

