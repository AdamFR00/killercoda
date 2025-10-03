# Step 4: Provisioning our Prometheus datasource
Now that we have our Grafana and Prometheus services running, we need to configure Grafana to use Prometheus as a data source. This will allow us to visualize the metrics collected by Prometheus in Grafana.

## Using a Provisioning File
1. We have already created a provisioning file for you. We will move this file to the correct location and restart the Grafana service. Run the following command to do this:
   ```
   sudo cp /education/prometheus_datasource.yml /etc/grafana/provisioning/datasources/ && sudo systemctl restart grafana-server
   ```{{execute}}

3. Open your browser and go to the Grafana UI by clicking on the following link: **[http://localhost:3000]({{TRAFFIC_HOST1_3000}})**

4. Sign in with the following credentials:
   - **Username:** admin
   - **Password:** admin
