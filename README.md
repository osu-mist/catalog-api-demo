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
	$ docker run \
	> --name=catalog_api_demo \
	> --publish 8000:8000 \
	> --volume /path/to/configuration.json:/demo/catalog-api-demo/configuration.json:ro \
	> catalog_api_demo
	```

Docker Swarm (1.2.5)
------------

This section shows how to deploy this application with [Docker Swarm](https://docs.docker.com/swarm/).
You can check you swarm version by running `docker run --rm swarm -v`.

#### Create a swarm cluster

Prepare multiple machines as nodes in swarm cluster. I am going to use [VirtulBox](https://www.virtualbox.org/) here to create three `manager nodes` and seven `worker nodes` as an example. According to [Docker documentation](https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/), it is recommended to have odd number of nodes according to the organization’s high-availability requirements.

> * A three-manager swarm tolerates a maximum loss of one manager.
> * An N manager cluster will tolerate the loss of at most (N-1)/2 managers.
> * Docker recommends a maximum of seven manager nodes for a swarm.

```
$ docker-machine create --driver virtualbox manager01
$ docker-machine create --driver virtualbox manager02
$ docker-machine create --driver virtualbox manager03
$ docker-machine create --driver virtualbox worker01
$ docker-machine create --driver virtualbox worker02
...
$ docker-machine create --driver virtualbox worker07
```

After creating machines, you can list all machines you have by typing:

```
$ docker-machine ls

NAME        ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER    ERRORS
manager01   -        virtualbox   Running   tcp://<manager01_ip>:2376           v1.12.3
manager02   -        virtualbox   Running   tcp://<manager02_ip>:2376           v1.12.3
manager03   -        virtualbox   Running   tcp://<manager03_ip>:2376           v1.12.3
worker01    -        virtualbox   Running   tcp://<worker01_ip>:2376            v1.12.3
worker02    -        virtualbox   Running   tcp://<worker02_ip>:2376            v1.12.3
...
worker07    -        virtualbox   Running   tcp://<worker07_ip>:2376            v1.12.3
```

#### Initialize a swarm

Now we are going to login into the manager machine and have it become the primary `manager node` in the swarm cluster.

```
$ MANAGER01_IP=$(docker-machine ip manager01)
$ docker-machine ssh manager01 docker swarm init --advertise-addr $MANAGER01_IP:2377

Swarm initialized: current node (<node_id>) is now a manager.

To add a worker to this swarm, run the following command:

	docker swarm join \
	--token <worker_node_token> \
	<manager01_ip>:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

Make sure you have the swarm token after you initializing it. We will need the token later, but please **DO NOT** store it as an environment variable. 

#### Add manager nodes to the swarm

We can also add more `manager nodes` to our swarm.

```
$ docker-machine ssh manager01 docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token <manager_node_token> \
    <manager01_ip>:2377
```

```
$ docker-machine ssh manager02 docker swarm join \
> --token <manager_node_token> \
> <manager01_ip>:2377
```

Repeat this process to add all the other two managers to the cluster.

#### Add worker nodes to the swarm

The following is an example that adding `worker01`, `worker02` and `worker03` to `manager01`. Use the following command to get the token first:

```
$ docker-machine ssh manager01 docker swarm join-token worker

To add a worker to this swarm, run the following command:

	docker swarm join \
	--token <worker_node_token> \
	<manager01_ip>:2377
```

Now add `worker nodes` to `manager01`:

```
$ WORKER01_IP=$(docker-machine ip worker01)
$ docker-machine ssh worker01 docker swarm join \
> --token <worker_node_token> \
> $MANAGER01_IP:2377
```

Repeat this process to construct our cluster structure as following:
`worker01`, `worker02` and `worker03` to `manager01`;
`worker04` and `worker05` to `manager02`;
`worker06` and `worker07` to `manager03`

#### List all nodes in the swarm

You are allowed to check every nodes status in a swarm via the `manager node`.

```
$ docker-machine ssh manager01 docker node ls

ID                     HOSTNAME   STATUS  AVAILABILITY  MANAGER STATUS
<manager01_node_id> *  manager01  Ready   Active        Leader
<worker01_node_id>     worker01   Ready   Active
<worker02_node_id>     worker02   Ready   Active
<worker03_node_id>     worker03   Ready   Active
<manager02_node_id>    manager02  Ready   Active        Reachable
<worker04_node_id>     worker04   Ready   Active
<worker05_node_id>     worker05   Ready   Active
<manager03_node_id>    manager03  Ready   Active        Reachable
<worker06_node_id>     worker06   Ready   Active
<worker07_node_id>     worker07   Ready   Active
```

#### Deploy a service to manager nodes

1. Clone this repo to your `manager node` and prepare a proper `configuration.json` file.

2. Build the `catalog_api_demo` image on you `manager01`:

	```
	docker-machine ssh manager01 docker build --tag="catalog_api_demo" /path/to/catalog-api-demo
	```

2. Create a `catalog_api_demo` service on your `manager01`:

	```
	$ docker-machine ssh manager01 docker service create \
	> --name catalog_api_demo \
	> --replicas 10 \
	> --publish 8000:8000 \
	> --mount type=bind,src=/path/to/configuration.json,dst=/demo/catalog-api-demo/configuration.json,readonly \
	> catalog_api_demo
	```

	_* Note that `--replicas` is the number of instances of the image specified. You can scale your services by using the following command:_

	```
	$ docker-machine ssh manager01 docker service scale catalog_api_demo=<number_of_replicas>
	```

3. You can list all services on you `manager01`:

	```
	$ docker-machine ssh manager01 docker service ls

	ID            NAME              REPLICAS  IMAGE             COMMAND
	<service_id>  catalog_api_demo  3/15      catalog_api_demo
	```

4. Now you should be able to access the service through `manager01`:

	```
	$ curl -I http://<manager01_ip>:8000/catalog_api_demo/

	HTTP/1.0 200 OK
	Date: Tue, 01 Nov 2016 17:16:51 GMT
	Server: WSGIServer/0.1 Python/2.7.12
	X-Frame-Options: SAMEORIGIN
	Content-Type: text/html; charset=utf-8
	```

_* Note that in order to handle the situation if the leader node (primary manager node) down for some reason, we should build the images on multiple manager nodes. However, it is no need to create multiple services on them. Be aware that in three-manager swarm, the maximum loss of manager is only one._