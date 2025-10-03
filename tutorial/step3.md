# Step 3: Provisioning our Prometheus datasource
Now that we have our Grafana and Prometheus services running, we need to configure Grafana to use Prometheus as a data source. This will allow us to visualize the metrics collected by Prometheus in Grafana.

## Using a Provisioning File

1. We have already created a provisioning file for you. We will move this file to the correct location and restart the Grafana service. Run the following command to do this:
   ```
   sudo cp /education/prometheus_datasource.yml /etc/grafana/provisioning/datasources/ && sudo systemctl restart grafana-server
   ```{{execute}}

## Explain Provisioning File
