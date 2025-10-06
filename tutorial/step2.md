## Step 2: Prometheus

1. Download the latest version of Prometheus from the [Prometheus download page](https://prometheus.io/download/) using wget.
    ```
    wget https://github.com/prometheus/prometheus/releases/download/v2.50.1/prometheus-2.50.1.linux-amd64.tar.gz
    ```{{exec}}

2. Extract the tarball and navigate to the extracted directory. Move to bin directory.
    ```
    tar -xvf prometheus-2.50.1.linux-amd64.tar.gz && cd prometheus-2.50.1.linux-amd64 && sudo cp prometheus /usr/local/bin
    ```{{exec}}

3. Lets turn Prometheus into a service.
    ```
    sudo useradd -rs /bin/false prometheus && sudo mkdir /etc/prometheus /var/lib/prometheus && sudo cp /assets/prometheus.yml /etc/prometheus/prometheus.yml && sudo cp -r consoles/ console_libraries/ /etc/prometheus/ && sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus && echo -e "[Unit]\nDescription=Prometheus\nAfter=network.target\n\n[Service]\nUser=prometheus\nGroup=prometheus\nType=simple\nExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/var/lib/prometheus --web.console.templates=/etc/prometheus/consoles --web.console.libraries=/etc/prometheus/console_libraries\n\n[Install]\nWantedBy=multi-user.target" | sudo tee /etc/systemd/system/prometheus.service > /dev/null && sudo systemctl daemon-reload && sudo systemctl start prometheus
    ```{{exec}}

Let's break it down:
```bash
    sudo useradd -rs /bin/false prometheus
```
Adds a system account for prometheus shown by -r. Usally, a user is given a login shell such as /bin/bash or /bin/sh. But as this is only an account for prometheus we disable the login option by adding a shell that immediatly exits -s /bin/false.
```bash
    sudo mkdir /etc/prometheus /var/lib/prometheus && sudo cp prometheus.yml /etc/prometheus/prometheus.yml
```
Creates necessary prometheus directories
```bash
sudo cp /assets/prometheus.yml /etc/prometheus/prometheus.yml
sudo cp -r consoles/ console_libraries/ /etc/prometheus/
``` 
Copy our config file `/assets/prometheus.yml` into our directory, you can find it here: [prometheus.yml](https://github.com/jsoderholm/killercoda/blob/main/tutorial/assets/prometheus.yml)(Or further down the page) and copy the html console templates into our directory. 
```bash
sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus 
```
Makes the user prometheus the owner of the directories.
```bash
echo -e "[Unit]
Description=Prometheus
After=network.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target" \
| sudo tee /etc/systemd/system/prometheus.service > /dev/null
```
Here we create the /etc/systemd/system/prometheus.service. 
[Unit] - creates the metadata for the service. 
[Service] - defines how the prometheus should run. 
[Install] - Makes prometheus start on boot. 
```bash
    sudo systemctl daemon-reload && sudo systemctl start prometheus
```
Then we reload the systemd configuration files and start the prometheus service.  
4. Your `/etc/prometheus/prometheus.yml` should look like this:
```bash
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
5. Verify Prometheus is running:
   Visit [http://localhost:9090]({{TRAFFIC_HOST1_9090}}).
   You should see the Prometheus web interface.

   - Head to **Status → Targets** (`http://localhost:9090/targets`)
   - Confirm that the **cAdvisor** is listed and **UP**.

---