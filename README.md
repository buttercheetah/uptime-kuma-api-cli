# UptimeKuma Incident Management Script

This script allows you to manage incidents on UptimeKuma status pages. It provides functionality to create, update, and clear incidents using predefined templates based on different power outage scenarios. The script is powered by the `uptime_kuma_api` library and takes configuration information from a YAML config file.

## Prerequisites

- Python 3.x
- `uptime_kuma_api` library (Install using `pip install uptime-kuma-api`)

## Usage

Run the script with the following command:

```bash
python script_name.py config_file action slug
```
 - config_file: Path to the YAML config file containing UptimeKuma configuration.

 - action: The action you want to perform. Available actions are:
     - small_power: Begin a power outage incident.
     - medium_power: Indicate an extended power outage.
     - large_power: Indicate a prolonged power outage before server shutdown.
     - power_returned: Mark the end of a power outage.
     - clear: Remove a pinned incident from UptimeKuma.
     - slug: The slug of the page you want to modify.

## Configuration
Create a YAML config file (e.g., config.yaml) with the following structure:
yaml
```
url: https://your-uptimekuma-instance.com
login:
  username: your_username
  password: your_password
```

Ensure that a template.yaml file is present in the same directory as the script. This file should contain templates for incident messages based on different scenarios.

## Example
 - To create a "small_power" incident on a page with slug "example-page," run:
```bash
python script_name.py config.yaml small_power example-page
```
 - To clear an incident on a page with slug "example-page," run:
```bash
python script_name.py config.yaml clear example-page
```
##Notes
 - Make sure to provide the correct configuration and slug information for your UptimeKuma instance.
 - The script provides options to overwrite existing incidents.
 - Always review and adapt the script to your specific use case before running it in production.
