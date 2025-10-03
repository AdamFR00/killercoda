## Step 3: Installing Grafana

In this step, we will install Grafana on within our virtual environment. Grafana is an open-source platform for monitoring and observability that allows you to create, explore, and share dashboards and data visualizations.

### Installing Grafana

1. Let's install Grafana via apt install.
    ```
    sudo apt-get install -y apt-transport-https software-properties-common wget &&
    sudo mkdir -p /etc/apt/keyrings/ &&
    wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null &&
    echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list &&
    sudo apt-get update && sudo apt-get install -y grafana
    ```{{exec}}

    This command sequence adds the Grafana repository to your system's package manager.

    - It installs necessary packages (`apt-transport-https`, `software-properties-common`, `wget`).
    - It downloads the Grafana GPG key, imports it, and saves it to the correct keyring location. This key verifies the authenticity of Grafana packages.
    - It adds the Grafana repository URL to your system's list of sources.
    - Finally, it updates the package list and installs the `grafana` package.

2. Let's make sure our Grafana service is running.
    ```
    sudo systemctl start grafana-server &&
    sudo systemctl status grafana-server
    ```{{exec}}

We should now be able to access Grafana by visiting the following URL in your browser: **[http://localhost:3000]({{TRAFFIC_HOST1_3000}})**. If you see a page with a login prompt, then Grafana is running correctly.

**Note:** It might take approximately 30 seconds for the Grafana service to fully start up after executing these commands. Please be patient before attempting to access the URL.
