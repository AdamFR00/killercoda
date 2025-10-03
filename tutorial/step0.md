## Step 0: Preparing the Application Environment


Before we set up our monitoring stack (Prometheus, Grafana, cAdvisor), we first need a sample application to monitor. The application will be used to demonstrate the capabilities of our observability tools.

First, we'll prepare a simple Flask web application, encapsulating it within a Docker container.

---

### Setting Up the Flask Application Files

Create a dedicated directory for our Flask application and copy the necessary files into it. These files include `app.py`, which contains our Flask application logic, and `Dockerfile`, which defines how to build the container image. For more information take a look at `assets/app.py`and `assets/Dockerfile`.

```
mkdir flask-app &&
sudo cp /education/app.py /education/Dockerfile flask-app/
```{{exec}}

---

### Building the Flask App Docker Image

Now that the application files are in place, the next step is to build a Docker image. This image will package our Flask application with all its required dependencies into a single unit.

```
cd flask-app &&
docker build -t flask-app .
```{{exec}}

---

### Running the Flask App in a Container

With our Docker image successfully built, we will now run it as a container. This will spin up our Flask application in an isolated Docker environment.

In this command we: start the container and map its internal port `5000` to your host machine's port `5000`. This allows you to access the application from your browser.

```bash
docker run -d --name flask-app \
  -p 5000:5000 \
  --restart unless-stopped \
  flask-app
```{{exec}}

To verify that our container is running and is active, we can use the following command:

```bash
docker ps
```{{exec}}

---

### Testing the Flask App Locally

Before proceeding to set up the monitoring stack, we can confirm that our Flask application is accessible and functioning correctly by visiting: **[http://localhost:5000]({{TRAFFIC_HOST1_5000}})**.

---

### Next Steps

We have now successfully prepared and deployed our sample Flask application in a Docker container.

In the subsequent steps, we will proceed to build our container observability stack:

1.  **Set up cAdvisor**
2.  **Configure Prometheus**
3.  **Install and Configure Grafana**
