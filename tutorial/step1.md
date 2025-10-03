## Step 1: cAdvisor

Before we can start visualizing our data in Grafana, we need to collect metrics from our running containers. While Prometheus can scrape any endpoint that exposes metrics, it doesn’t provide deep container insights by itself.
---
cAdvisor provides detailed resource usage and performance characteristics of running containers (CPU, memory, disk, network metrics). It exposes metrics at an HTTP endpoint that Prometheus can consume directly.

1. Run cAdvisor using Docker:

   ```bash
   docker run \
     --volume=/:/rootfs:ro \
     --volume=/var/run:/var/run:ro \
     --volume=/sys:/sys:ro \
     --volume=/var/lib/docker/:/var/lib/docker:ro \
     --publish=8080:8080 \
     --detach=true \
     --name=cadvisor \
     gcr.io/cadvisor/cadvisor:latest
   ```{{exec}}
First we give cAdvisor Read-Only (:ro) access to some important directories on our machine using the ---volume command. Let's walk you through each instance:
```bash
--volume=/:/rootfs:ro
```
Gives access to the hosts root filesystem in order for cAdvisor to inspect files.
```bash
--volume=/var/run:/var/run:ro
```
Gives access to the Docker socket & runtime info.
```bash
--volume=/sys:/sys:ro
```
Gives access to kernel system metrics (CPU, memory)
```bash
--volume=/var/lib/docker/:/var/lib/docker:ro
```
This enables cAdvisor to view Docker container metadata.
```bash
--publish=8080:8080
```
The data from cAdvisor will be available on the hosts port 8080.
```bash
--detach=true
```
Enables cAdvisor to run in the background.
Finally we name the container and provide the cAdvisor docker image from Google's container registry.
```bash
--name=cadvisor \
gcr.io/cadvisor/cadvisor:latest
```
2. Verify cAdvisor is running by visiting:
   [http://localhost:8080]({{TRAFFIC_HOST1_8080}})
   You should see a simple web interface and metrics being exposed.


## ✅ Summary

- **cAdvisor** exposes container-level metrics on port `8080`.

Now that we have metrics available from cAdvisor, we need a way to scrape and store them. This is where **Prometheus** comes in.
