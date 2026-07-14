Docker Container Management

## Managing container lifecycle

Docker provides several commands for managing the lifecycle of containers: starting, stopping, restarting, pausing, and removing them.

---

## docker restart

The `docker restart` command stops and then starts one or more containers.

```
docker restart [OPTIONS] CONTAINER [CONTAINER...]
```

### Options

| Option | Description |
|---|---|
| `--time`, `-t` | Seconds to wait before killing the container (default: 10) |
| `--signal`, `-s` | Signal to send to the container |

### Examples

Restart a running container named `my_container`:

```
docker restart my_container
```

Restart multiple containers at once:

```
docker restart container1 container2 container3
```

Restart with a custom timeout (wait 5 seconds before force-killing):

```
docker restart --time 5 my_container
```

Restart using the container ID:

```
docker restart a1b2c3d4e5f6
```

---

## docker stop

The `docker stop` command sends a SIGTERM signal to the main process inside the container, then waits for it to exit gracefully. If it does not exit within the timeout, a SIGKILL is sent.

```
docker stop [OPTIONS] CONTAINER [CONTAINER...]
```

### Options

| Option | Description |
|---|---|
| `--time`, `-t` | Seconds to wait before sending SIGKILL (default: 10) |
| `--signal`, `-s` | Signal to send to the container |

### Examples

Stop a running container:

```
docker stop my_container
```

Stop with a shorter grace period:

```
docker stop --time 5 my_container
```

Stop all running containers:

```
docker stop $(docker ps -q)
```

---

## docker start

The `docker start` command starts one or more stopped containers.

```
docker start [OPTIONS] CONTAINER [CONTAINER...]
```

### Options

| Option | Description |
|---|---|
| `--attach`, `-a` | Attach STDOUT/STDERR and forward signals |
| `--interactive`, `-i` | Attach container's STDIN |

### Examples

Start a stopped container:

```
docker start my_container
```

Start and attach to the container output:

```
docker start --attach my_container
```

---

## docker kill

The `docker kill` command sends a SIGKILL (or specified signal) immediately to the container without a grace period.

```
docker kill [OPTIONS] CONTAINER [CONTAINER...]
```

### Examples

Force kill a container immediately:

```
docker kill my_container
```

Send a custom signal:

```
docker kill --signal SIGINT my_container
```

---

## docker pause and docker unpause

The `docker pause` command suspends all processes in a container using the cgroups freezer. The `docker unpause` command resumes them.

```
docker pause CONTAINER [CONTAINER...]
docker unpause CONTAINER [CONTAINER...]
```

### Examples

Pause a container:

```
docker pause my_container
```

Unpause a container:

```
docker unpause my_container
```

---

## docker rm

The `docker rm` command removes one or more stopped containers.

```
docker rm [OPTIONS] CONTAINER [CONTAINER...]
```

### Options

| Option | Description |
|---|---|
| `--force`, `-f` | Force remove a running container (sends SIGKILL) |
| `--volumes`, `-v` | Remove anonymous volumes attached to the container |

### Examples

Remove a stopped container:

```
docker rm my_container
```

Force remove a running container:

```
docker rm --force my_container
```

Remove all stopped containers:

```
docker rm $(docker ps -aq -f status=exited)
```

---

## Restart policies

You can configure a container to automatically restart using the `--restart` flag with `docker run`.

```
docker run --restart=always my_image
```

### Restart policy options

| Policy | Description |
|---|---|
| `no` | Do not automatically restart (default) |
| `on-failure[:max-retries]` | Restart only if the container exits with a non-zero code |
| `always` | Always restart regardless of exit code |
| `unless-stopped` | Always restart unless the container was explicitly stopped |

### Examples

Run a container that always restarts:

```
docker run -d --restart=always nginx
```

Run a container that restarts on failure up to 5 times:

```
docker run -d --restart=on-failure:5 my_app
```

---

## Listing containers

Use `docker ps` to see running containers and `docker ps -a` to see all containers including stopped ones.

```
docker ps
docker ps -a
docker ps -a --filter "status=exited"
```

---

## Common workflow: restart a container

To restart a running container named `web`:

```
docker restart web
```

To stop and start manually:

```
docker stop web
docker start web
```

To see the status of containers:

```
docker ps -a
```

To view logs after restarting:

```
docker logs web
docker logs --follow web
```
