# Step 0: Preparing the Application Environment


Welcome to our container observability tutorial! Before we dive into setting up our monitoring stack (Prometheus, Grafana, cAdvisor), we first need a sample application to monitor.

In this step, we’ll prepare a simple Flask web application inside a Docker container. This application will have routes to simply serve content and, crucially, to simulate a CPU workload.

## Lorem

```
sudo cp -r /education/flask flask-app
```{{exec}}
