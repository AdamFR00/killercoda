# Step 1: Collecting Metrics

Before we can start visualizing our data, we need to collect some metrics from our running containers. Prometheus on its own cannot reach into container runtimes to show CPU, memory, disk, and network usage at a container level.
For this reason, we will use **cAdvisor** (Container Advisor) together with **Prometheus**.

**Note:** When asked to go to a specific port, click on the link provided in the terminal. This will redirect you to the correct URL for this training instance.

---

## cAdvisor

cAdvisor (Container Advisor) provides detailed resource usage and performance characteristics of running containers. It’s lightweight, comes from the Kubernetes ecosystem, and gives Prometheus metrics out-of-the-box.

Let’s install and run cAdvisor inside our environment:

1. Run cAdvisor (we’ll use Docker to keep it simple):

   ````bash
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

   ````

2. Verify that cAdvisor is running by visiting:
   [http://localhost:8080]({{TRAFFIC_HOST1_8080}})
   You should see a simple web UI and metrics being exported.

---

## Prometheus

Prometheus is a monitoring and alerting toolkit that we will use to scrape and store cAdvisor’s container metrics.

1. Download the latest version of Prometheus:

   ````bash
   wget https://github.com/prometheus/prometheus/releases/download/v2.50.1/prometheus-2.50.1.linux-amd64.tar.gz
   ```{{exec}}

   ````

2. Extract and copy the binary:

   ````bash
   tar -xvf prometheus-2.50.1.linux-amd64.tar.gz \
     && cd prometheus-2.50.1.linux-amd64 \
     && sudo cp prometheus /usr/local/bin
   ```{{exec}}

   ````

3. Create the Prometheus user, directories, and service:

   ````bash
   sudo useradd -rs /bin/false prometheus
   sudo mkdir /etc/prometheus /var/lib/prometheus
   sudo cp prometheus.yml /etc/prometheus/prometheus.yml
   sudo cp -r consoles/ console_libraries/ /etc/prometheus/
   sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus

   echo -e "[Unit]\nDescription=Prometheus\nAfter=network.target\n\n[Service]\nUser=prometheus\nGroup=prometheus\nType=simple\nExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/var/lib/prometheus --web.console.templates=/etc/prometheus/consoles --web.console.libraries=/etc/prometheus/console_libraries\n\n[Install]\nWantedBy=multi-user.target" \
     | sudo tee /etc/systemd/system/prometheus.service > /dev/null

   sudo systemctl daemon-reload
   sudo systemctl start prometheus
   ```{{exec}}

   ````

4. Update the Prometheus configuration to scrape metrics from cAdvisor. Your `prometheus.yml` should look like this:

   ```yaml
   global:
     scrape_interval: 5s
     evaluation_interval: 5s

   scrape_configs:
     - job_name: "cadvisor"
       static_configs:
         - targets: ["0.0.0.0:8080"]
   ```

   Copy this file into place and restart Prometheus:

   ````bash
   sudo cp /education/prometheus.yml /etc/prometheus/prometheus.yml
   sudo systemctl restart prometheus
   ```{{exec}}
   ````

---

## Verify Setup

Visit the Prometheus UI at:
[http://localhost:9090]({{TRAFFIC_HOST1_9090}})

- Go to the **Targets** page under _Status_ → you should see `cadvisor` as an active target.
- Prometheus is now scraping container metrics from cAdvisor successfully!
