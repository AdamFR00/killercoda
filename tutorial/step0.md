# Step 0: Preparing the Application Environment


Welcome to our container observability tutorial! Before we dive into setting up our monitoring stack (Prometheus, Grafana, cAdvisor), we first need a sample application to monitor.

In this step, we’ll prepare a simple Flask web application inside a Docker container. This application will have routes to simply serve content and, crucially, to simulate a CPU workload.

---

## 1. Lorem

```
mkdir flask-app && sudo cp /education/app.py /education/Dockerfile flask-app/
```{{exec}}

---

## 2. Build the Flask App Docker Image

We will now build a Docker image from the provided Dockerfile. This image will contain our Flask application and its dependencies.

Navigate to the directory containing the files and build the image:

```
cd flask-app &&
docker build -t flask-app .
```{{exec}}

---

## 3. Run the Flask App in a Container

Once the image is built, we’ll run it as a container. This container will host our Flask application.

Start the container, mapping port `5000` from the container to your host machine:

```bash
docker run -d --name flask-app -p 5000:5000 flask-app
```{{exec}}

You can verify that the container is running:

```bash
docker ps
```{{exec}}

---

## 4. Test the Flask App Locally

Before we move to setting up monitoring, let's quickly confirm our Flask app is accessible:

- Visit [http://localhost:5000]({{TRAFFIC_HOST1_5000}}) → You should see:
  **“Flask app is running!”**

- Visit [http://localhost:5000/cpu-stress]({{TRAFFIC_HOST1_5000}}) → This route will intentionally cause a high CPU load within the container for about 5 seconds. This is what we’ll later monitor.

---

## ✅ Next Steps

We have successfully prepared our application. In the subsequent steps, we will:

1.  Set up **cAdvisor** to collect container-level metrics.
2.  Configure **Prometheus** to scrape metrics from cAdvisor.
3.  Install and configure **Grafana** to visualize these metrics.

This initial step ensures we have a containerized workload ready to be monitored by the stack we will build.

---

👉 **Important Note:** You do **not** need to install Flask on your host machine. Flask is installed inside the Docker container itself during the `docker build` process, making the setup self-contained and reproducible.

---
