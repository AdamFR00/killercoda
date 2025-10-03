# Step 0: Preparing the Application Environment


Before we delve into setting up our monitoring stack (Prometheus, Grafana, cAdvisor), we first need a sample application to monitor. This foundation will allow us to effectively demonstrate and observe the capabilities of our observability tools.

In this initial step, we'll prepare a simple Flask web application, encapsulating it within a Docker container.

---

## 1. Setting Up the Flask Application Files

First, we will create a dedicated directory for our Flask application and copy the necessary files into it. These files include `app.py`, which contains our Flask application logic, and `Dockerfile`, which defines how to build our container image.

```
mkdir flask-app &&
sudo cp /education/app.py /education/Dockerfile flask-app/
```{{exec}}

---

## 2. Building the Flask App Docker Image

Now that our application files are in place, the next step is to build a Docker image. This image will package our Flask application along with all its required dependencies into a single, portable unit.

```
cd flask-app &&
docker build -t flask-app .
```{{exec}}

---

## 3. Running the Flask App in a Container

With our Docker image successfully built, we will now run it as a container. This action will spin up our Flask application in an isolated Docker environment.

Start the container, mapping its internal port `5000` to your host machine's port `5000`. This allows you to access the application from your browser.

```bash
docker run -d --name flask-app \
  -p 5000:5000 \
  --restart unless-stopped \
  flask-app
```{{exec}}

To verify that the container is running and active, use the following command:

```bash
docker ps
```{{exec}}

---

## 4. Testing the Flask App Locally

Before proceeding to set up our monitoring stack, let's quickly confirm that our Flask application is accessible and functioning correctly:

- **Access the main application page:** Visit [http://localhost:5000]({{TRAFFIC_HOST1_5000}})
    - You should see the message: **“Flask app is running!”** This confirms the application is serving content.

---

## Next Steps

You have successfully prepared and deployed our sample Flask application in a Docker container. This establishes the essential workload we need for our observability exercise.

In the subsequent steps, we will proceed to build our robust container observability stack:

1.  **Set up cAdvisor:** We will deploy cAdvisor to gather detailed, real-time resource metrics directly from our running containers, providing crucial low-level insights.
2.  **Configure Prometheus:** We will then set up Prometheus to reliably scrape and store these valuable metrics exposed by cAdvisor.
3.  **Install and Configure Grafana:** Finally, we will install Grafana and create compelling dashboards to visualize and analyze the collected metrics, transforming raw data into actionable insights.
