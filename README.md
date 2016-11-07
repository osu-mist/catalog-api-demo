Catalog API Demo
================

Demo of course catalog related APIs:

1. [Class Search API](https://github.com/osu-mist/class-search-api)
2. [Terms API](https://github.com/osu-mist/terms-api)
3. [Course Subjects API](https://github.com/osu-mist/course-subjects-api)

Installation
------------

This application is implemented with [Django](https://www.djangoproject.com/) framework ([version 1.10.1](https://docs.djangoproject.com/en/1.10/releases/1.10.1/)), so make sure you have installed Django first. You can simply install it with [pip](https://pip.pypa.io/en/latest/):
	
```
$ pip install Django==1.10.1
```

Configuration
-------------

1. Register your application to use the Class Search API, Course Subjects API, and Terms API at the [OSU Developer Portal](https://developer.oregonstate.edu/).
2. Put your `configuration.json` file which contains `client_id` and `client_secret` in the root folder of this application.

	```json
	"client_id": "secret",
	"client_secret": "sauce"
	```

Usage
-----

1. Execute the following commands to run the server:

	```
	$ cd catalog_api_demo
	$ python manage.py runserver
	```

2. While the server is running locally, visit `http://127.0.0.1:8000/catalog_api_demo/` with your Web browser.

Docker (1.12.1)
---------------

1. Build the docker image by running:
	
	```
	$ docker build --tag="catalog_api_demo" .
	```
	
	**Warning:** Do not put your `configuration.json` file in the root of the application when building the image. You should mount the configuration file as a readonly volume.

2. Run the docker container:
	
	```
	$ docker run --name=catalog_api_demo --publish 8000:8000 --volume /path/to/configuration.json:/demo/catalog-api-demo/configuration.json:ro catalog_api_demo
	```

Docker Swarm (1.2.5)
------------

This section shows how to deploy this application with [Docker Swarm](https://docs.docker.com/swarm/).
You can check you swarm version by running `docker run --rm swarm -v`.

#### Create a swarm cluster

Prepare multiple machines as nodes in swarm cluster. I am going to use [VirtulBox](https://www.virtualbox.org/) here to create one `manager node` and one `worker node` locally as an example. You can create as many nodes as you need.

```
$ docker-machine create --driver virtualbox manager
$ docker-machine create --driver virtualbox worker
```

After creating machines, you can list all machines you have by typing:

```
$ docker-machine ls

NAME      ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER    ERRORS
manager   -        virtualbox   Running   tcp://<manager_ip>:2376             v1.12.3
worker    -        virtualbox   Running   tcp://<worker_ip>:2376              v1.12.3
```

#### Initialize a swarm

Now we are going to login into the manager machine and have it become the `manager node` in the swarm cluster.

```
$ MANAGER_IP=$(docker-machine ip manager)
$ docker-machine ssh manager docker swarm init --advertise-addr $MANAGER_IP:2377

Swarm initialized: current node (<node_id>) is now a manager.

To add a worker to this swarm, run the following command:

	docker swarm join \
	--token <token> \
	<manager_ip>:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

Make sure you have the swarm token after you initializing it. We will need the token later, but please **DO NOT** store it as an environment variable. 

#### Add nodes to the swarm

We have already initialize a swarm with one `manager node` from previous step. Now we are going to add the worker machine as `worker node` to our swarm cluster.

```
$ WORKER_IP=$(docker-machine ip worker)
$ docker-machine ssh worker docker swarm join --token <token> $WORKER_IP:2377
```

#### List all nodes in the swarm

You are allowed to check every nodes status in a swarm.

```
$ docker-machine ssh manager docker node ls

ID                   HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
<manager_node_id> *  manager   Ready   Active        Leader
<workder_node_id>    worker    Ready   Active
```

#### Deploy a service to worker nodes

1. Clone this repo to your `manager node` and prepare a proper `configuration.json` file.

2. Build the `catalog_api_demo` image in you `manager node`:

	```
	docker-machine ssh manager docker build --tag="catalog_api_demo" <path_to_catalog_api_demo_repo>
	```

2. Create a `catalog_api_demo` service on your `manager node`:

	```
	$ docker-machine ssh manager docker service create --name catalog_api_demo --replicas 4 --publish 8000:8000 --volume /path/to/configuration.json:/demo/catalog-api-demo/configuration.json:ro catalog_api_demo
	```

	_* Note that `--replicas` is the number of instances of the image specified._

3. You can list all services on you `manager node`:

	```
	$ docker-machine ssh manager docker service ls

	ID            NAME              REPLICAS  IMAGE             COMMAND
	<service_id>  catalog_api_demo  1/4       catalog_api_demo
	```

4. Now you should be able to access the service through `manager node`:

	```
	$ curl -I http://<manager_ip>:8000/catalog_api_demo/

	HTTP/1.0 200 OK
	Date: Tue, 01 Nov 2016 17:16:51 GMT
	Server: WSGIServer/0.1 Python/2.7.12
	X-Frame-Options: SAMEORIGIN
	Content-Type: text/html; charset=utf-8
	```