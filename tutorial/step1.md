# Step 1: Collecting Metrics

Before we can start visualizing our data in Grafana, we need to **collect metrics** from our running containers. While Prometheus can scrape any endpoint that exposes metrics, it doesn’t provide deep container insights by itself.

For container-level observability, we will use **cAdvisor (Container Advisor)**, combined with **Prometheus** to scrape, store, and query container metrics.

---

**Note:** When asked to go to a specific port, always click the link provided in the terminal. This will redirect you to the correct URL for this training environment.

---

## cAdvisor

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

2. Verify cAdvisor is running by visiting:
   [http://localhost:8080]({{TRAFFIC_HOST1_8080}})
   You should see a simple web interface and metrics being exposed.

---

## Prometheus

Now that we have metrics available from cAdvisor, we need a way to scrape and store them. This is where **Prometheus** comes in.

1. Download and extract Prometheus:

   ```bash
   wget https://github.com/prometheus/prometheus/releases/download/v2.50.1/prometheus-2.50.1.linux-amd64.tar.gz
   tar -xvf prometheus-2.50.1.linux-amd64.tar.gz
   cd prometheus-2.50.1.linux-amd64
   sudo cp prometheus /usr/local/bin
   cd ..
   ```{{exec}}

2. Create a Prometheus user and necessary directories:

   ```bash
   sudo useradd -rs /bin/false prometheus
   sudo mkdir /etc/prometheus /var/lib/prometheus
   sudo cp -r prometheus-2.50.1.linux-amd64/consoles /etc/prometheus/
   sudo cp -r prometheus-2.50.1.linux-amd64/console_libraries /etc/prometheus/
   sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus
   ```{{exec}}

3. Create the Prometheus configuration file:

   ```bash
   cat <<EOF | sudo tee /etc/prometheus/prometheus.yml
   global:
     scrape_interval: 5s
     evaluation_interval: 5s

   scrape_configs:
     - job_name: "cadvisor"
       static_configs:
         - targets: ["0.0.0.0:8080"]
   EOF
   ```{{exec}}

4. Create the Prometheus systemd service:

   ```bash
   echo -e "[Unit]
   Description=Prometheus
   After=network.target

   [Service]
   User=prometheus
   Group=prometheus
   Type=simple
   ExecStart=/usr/local/bin/prometheus \\
     --config.file=/etc/prometheus/prometheus.yml \\
     --storage.tsdb.path=/var/lib/prometheus \\
     --web.console.templates=/etc/prometheus/consoles \\
     --web.console.libraries=/etc/prometheus/console_libraries

   [Install]
   WantedBy=multi-user.target" | sudo tee /etc/systemd/system/prometheus.service
   ```{{exec}}

5. Enable and start Prometheus:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable prometheus
   sudo systemctl start prometheus
   ```{{exec}}

6. Verify Prometheus is running:
   Visit [http://localhost:9090]({{TRAFFIC_HOST1_9090}}).
   You should see the Prometheus web interface.

   - Head to **Status → Targets** (`http://localhost:9090/targets`)
   - Confirm that the **cadvisor target** is listed and **UP**.

---

## ✅ Summary

- **cAdvisor** exposes container-level metrics on port `8080`.
- **Prometheus** scrapes these metrics every 5 seconds and stores them.
- We now have the base observability pipeline: **cAdvisor → Prometheus**.

In the next step, we will connect **Grafana** to Prometheus so that we can build dashboards and visualize container metrics interactively.
