# Agent Restart Automation

This repository contains a Python script (`elk2a_v3.py`) designed to automate the process of detecting specific alerts within an Elasticsearch/Kibana environment and subsequently executing predefined commands (e.g., agent restarts) on the affected hosts. It serves as a proactive, automated first-response system to keep critical agents or services running by addressing common issues flagged by your monitoring stack.

## Table of Contents

1.  [Description](https://www.google.com/search?q=%23description)
2.  [Features](https://www.google.com/search?q=%23features)
3.  [Prerequisites](https://www.google.com/search?q=%23prerequisites)
4.  [Installation](https://www.google.com/search?q=%23installation)
5.  [Configuration](https://www.google.com/search?q=%23configuration)
      * [1. `es_auth.json`](https://www.google.com/search?q=%231-es_authjson)
      * [2. `hostnames.txt`](https://www.google.com/search?q=%232-hostnamestxt)
      * [3. Command-Line Arguments](https://www.google.com/search?q=%233-command-line-arguments)
6.  [Usage](https://www.google.com/search?q=%23usage)
7.  [Logging](https://www.google.com/search?q=%23logging)
8.  [Security Considerations](https://www.google.com/search?q=%23security-considerations)
9.  [Contributing](https://www.google.com/search?q=%23contributing)
10. [License](https://www.google.com/search?q=%23license)

## Description

The `agent_restart_automation` project provides a robust solution for automating the remediation of issues that can be detected via Kibana alerts. Instead of requiring manual intervention from operations teams, this script continuously monitors Kibana's alert history for specific alert types. Upon detection, it identifies the affected host, applies configurable filters, and executes a pre-defined command on that host (e.g., restarting an agent process). This helps maintain service availability and reduces operational overhead.

## Features

  * **Kibana Alert Monitoring:** Connects to Kibana's alert history API to continuously check for `active` alerts of a configurable type.
  * **Host Identification:** Extracts the `host.name` from alert contexts to pinpoint the affected server.
  * **Host Filtering:** Supports an exclusion list (`hostnames.txt`) to prevent actions on specified critical or blacklisted hosts.
  * **Automated Command Execution:** Executes any specified shell command on the target host (e.g., `sudo systemctl restart my-agent`) using `subprocess.run`.
  * **State Persistence:** Utilizes a `last_processed_time.txt` file to remember the last timestamp alerts were processed, ensuring that only new, unhandled alerts trigger actions.
  * **Comprehensive Logging:** Records all activities, detected alerts, executed commands, and outcomes (success/failure) to a dedicated log file (`agent_restart.log`).
  * **Secure Authentication:** Uses Elasticsearch API keys for authentication, loaded from an external file (`es_auth.json`).
  * **Configurable:** Key parameters like Elasticsearch host, alert type, and restart command are configurable via command-line arguments.

## Prerequisites

Before deploying this script, ensure you have the following:

  * **Python 3.x:** Installed on the machine where the script will run.
  * **Python Libraries:**
      * `requests`
      * `elasticsearch` (the official Python client)
        You can install them using pip:
    <!-- end list -->
    ```bash
    pip install requests elasticsearch
    ```
  * **Elasticsearch & Kibana:** A running ELK stack (Elasticsearch and Kibana) with alerts configured and generating data in the `alerts` index.
  * **Elasticsearch API Key:** An API key with sufficient permissions to:
      * Read Kibana's alert history (e.g., `read` on `.alerts-*` index and `read` on the relevant Kibana API endpoints for alerts).
  * **Remote Host Access:** The machine running this script must have connectivity and appropriate authentication (e.g., SSH keys configured for passwordless access) to execute commands on the target hosts. The `restart-command` argument will be executed directly as a shell command.
  * **Permissions:** The user running the script needs file write permissions in its execution directory for `agent_restart.log` and `last_processed_time.txt`.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/olajio/agent_restart_automation.git
    cd agent_restart_automation
    ```

2.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The script's behavior is primarily configured via two external files and command-line arguments.

### 1\. `es_auth.json`

This file stores your Elasticsearch API Key credentials. **It is critical that this file is NOT committed to version control.**

  * Create a file named `es_auth.json` in the root directory of the script.

  * Add your API Key ID and Secret in the following JSON format:

    ```json
    {
      "api_key_id": "YOUR_ELASTICSEARCH_API_KEY_ID",
      "api_key_secret": "YOUR_ELASTICSEARCH_API_KEY_SECRET"
    }
    ```

    Replace `YOUR_ELASTICSEARCH_API_KEY_ID` and `YOUR_ELASTICSEARCH_API_KEY_SECRET` with your actual credentials.

### 2\. `hostnames.txt`

This file contains a list of hostnames that the script should **skip** when deciding to execute a command. This is useful for preventing automated actions on hosts that require manual intervention or are part of a different management system.

  * Create a file named `hostnames.txt` in the root directory of the script.

  * List one hostname per line:

    ```
    critical-server-01
    test-machine-exclude
    legacy-host
    ```

### 3\. Command-Line Arguments

The `elk2a_v3.py` script accepts the following command-line arguments:

  * `--es-host <URL>` (Required): The full URL of your Elasticsearch/Kibana instance (e.g., `https://your-kibana-host:5601`).
  * `--alert-type <STRING>` (Required): The exact string value of `kibana.alert.type` to monitor (e.g., "Agent has been offline", "VMware Guest CPU Usage").
  * `--restart-command <COMMAND>` (Required): The full shell command to execute on the detected host. This command will be run using `subprocess.run()`. **Ensure necessary SSH access and permissions are configured for this command to succeed.**
      * Example: `ssh -i /path/to/key.pem user@{} 'sudo systemctl restart myagent.service'`
      * Note: `{}` will be replaced by the detected hostname.
  * `--interval <SECONDS>` (Optional): The number of seconds to wait between each monitoring cycle. Default is 60 seconds.

## Usage

To run the script, navigate to the repository's root directory in your terminal and execute `elk2a_v3.py` with the required arguments:

```bash
python elk2a_v3.py \
  --es-host https://your-kibana.example.com:5601 \
  --alert-type "Agent has been offline" \
  --restart-command "ssh -o StrictHostKeyChecking=no admin@{hostname} 'sudo systemctl restart my-monitoring-agent.service'" \
  --interval 300
```

  * Replace placeholders like `https://your-kibana.example.com:5601`, `"Agent has been offline"`, and the `restart-command` with your actual values.
  * The `{hostname}` placeholder in `--restart-command` will be dynamically replaced by the actual hostname retrieved from the alert.
  * The script will run continuously until manually stopped (e.g., with `Ctrl+C`). It's recommended to run this script as a background service (e.g., using `systemd`, `nohup`, or a process manager like `pm2`) in a production environment.

## Logging

The script logs all its activities to `agent_restart.log` in the same directory where it is executed. This log file contains:

  * Timestamped entries for each action.
  * Information about alerts detected.
  * Confirmation of command execution or reasons for skipping.
  * Details on any errors encountered (e.g., network issues, command failures).

Monitor this log file regularly for insights into the script's operation and for troubleshooting.

## Security Considerations

  * **API Keys:** The `es_auth.json` file contains sensitive credentials. **NEVER commit `es_auth.json` to a public (or even private) Git repository.** Use `.gitignore` to prevent accidental commits. Consider more robust secret management solutions (e.g., environment variables, Vault, Kubernetes Secrets) for production deployments.
  * **`verify=False`:** The script uses `verify=False` for SSL connections to Elasticsearch/Kibana, which disables certificate verification. This is convenient for testing or environments with self-signed certificates, but it makes connections vulnerable to Man-in-the-Middle attacks. **For production deployments, remove `verify=False` and ensure your Python environment is configured to trust the SSL certificates of your Elasticsearch/Kibana instance.**
  * **`restart-command` Permissions:** The `restart-command` is executed directly on the host running the script. Ensure that the user running the script has appropriate SSH keys and permissions to execute the desired command (e.g., `sudo` access) on target systems without requiring password prompts. Carefully craft your `restart-command` to avoid unintended side effects.

## Contributing

Contributions are welcome\! If you have suggestions for improvements, bug fixes, or new features, please open an issue or submit a pull request.

## License

This project is open-sourced under the [MIT License](https://www.google.com/search?q=LICENSE).

-----
