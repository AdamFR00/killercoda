## Step 4: Provisioning Prometheus as a Grafana Data Source

Now that both Grafana and Prometheus are running, we need to connect them. This involves configuring Grafana to know __where__ to find Prometheus so it can fetch and visualize the metrics Prometheus is collecting. We'll do this using a Grafana provisioning file.

### Understanding Grafana Provisioning Files

Grafana uses configuration files to automatically set up data sources, dashboards, and other settings when Grafana starts. This is known as "provisioning." For data sources, a `datasources.yml` file (or similar) tells Grafana:

- `name`: A human-readable name for the data source (e.g., "Prometheus").

- `type`: The type of data source (e.g., `prometheus`).

- `access`: How Grafana should access the data source. `proxy` means Grafana acts as a proxy, making requests on behalf of the user to the data source's URL.

- `url`: The network address of the data source. In our case, it's **[http://localhost:9090]({{TRAFFIC_HOST1_9090}})**, where Prometheus is running.

- `isDefault`: If set to `true`, this data source will be automatically selected when you create a new dashboard panel.

The `prometheus_datasource.yml` file we are using is pre-configured to point to your Prometheus instance.

### Apply the Prometheus Data Source Configuration

We have already prepared a provisioning file for you. We'll move this file to Grafana's configuration directory and then restart the Grafana server to apply the changes.

Run the following command:

```
sudo cp /assets/prometheus_datasource.yml /etc/grafana/provisioning/datasources/ &&
sudo systemctl restart grafana-server
```{{execute}}

This command copies the `prometheus_datasource.yml` file into Grafana's datasource provisioning directory (`/etc/grafana/provisioning/datasources/`). To see the full file visit:[prometheus_datasource](https://github.com/jsoderholm/killercoda/blob/main/tutorial/assets/prometheus_datasource.yml). When Grafana starts up, it will read this file and automatically configure the Prometheus data source.
