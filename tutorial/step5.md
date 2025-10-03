# Step 4: Visualizing Container Metrics with Grafana

With Prometheus collecting metrics from cAdvisor and Grafana set up to use Prometheus as a data source, we can now create dashboards to visualize our container performance. We'll create panels to show CPU usage and memory usage for our `flask-app` container.

## 1. Create a New Grafana Dashboard

1. Open your Grafana UI by clicking [this link]({{TRAFFIC_HOST1_3000}}).
2. Sign in with your credentials:
    - **Username:** `admin`
    - **Password:** `admin`
3. In the left-hand menu, click the "+" **(Add)** icon, then select **"Dashboard"**.
4. Click on **"Add new panel"**

## 2. Panel: Container CPU Usage

This panel will show the CPU usage of our `flask-app` container.
