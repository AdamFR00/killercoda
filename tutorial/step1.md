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

1. Download the latest version of Prometheus from the [Prometheus download page](https://prometheus.io/download/).
    ```
    wget https://github.com/prometheus/prometheus/releases/download/v2.50.1/prometheus-2.50.1.linux-amd64.tar.gz
    ```{{exec}}

2. Extract the tarball and navigate to the extracted directory. Move to bin directory.
    ```
    tar -xvf prometheus-2.50.1.linux-amd64.tar.gz && cd prometheus-2.50.1.linux-amd64 && sudo cp prometheus /usr/local/bin
    ```{{exec}}

3. Lets turn Prometheus into a service (we will do the hard work for you).
    ```
    sudo useradd -rs /bin/false prometheus && sudo mkdir /etc/prometheus /var/lib/prometheus && sudo cp prometheus.yml /etc/prometheus/prometheus.yml && sudo cp -r consoles/ console_libraries/ /etc/prometheus/ && sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus && echo -e "[Unit]\nDescription=Prometheus\nAfter=network.target\n\n[Service]\nUser=prometheus\nGroup=prometheus\nType=simple\nExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/var/lib/prometheus --web.console.templates=/etc/prometheus/consoles --web.console.libraries=/etc/prometheus/console_libraries\n\n[Install]\nWantedBy=multi-user.target" | sudo tee /etc/systemd/system/prometheus.service > /dev/null && sudo systemctl daemon-reload && sudo systemctl start prometheus
    ```{{exec}}

4. Update the Prometheus configuration to scrape metrics from cAdvisor. Your `prometheus.yml` should look like this:
    ```
        # my global config
        global:
        scrape_interval: 5s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
        evaluation_interval: 5s # Evaluate rules every 15 seconds. The default is every 1 minute.
        # scrape_timeout is set to the global default (10s).

        # Alertmanager configuration
        alerting:
        alertmanagers:
            - static_configs:
                - targets:
                # - alertmanager:9093

        # Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
        rule_files:
        # - "first_rules.yml"
        # - "second_rules.yml"

        # A scrape configuration containing exactly one endpoint to scrape:
        scrape_configs:
        # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
        - job_name: "cAdvisor"

            # metrics_path defaults to '/metrics'
            # scheme defaults to 'http'.

            static_configs:
            - targets: ["0.0.0.0:8080"]

    ```

    We will copy this file to the /etc/prometheus directory and restart the prometheus service.

    ```
    sudo cp /education/prometheus.yml /etc/prometheus/prometheus.yml && sudo systemctl restart prometheus
    ```{{exec}}

5. Verify Prometheus is running:
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
