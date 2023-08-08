from uptime_kuma_api import UptimeKumaApi, MonitorType, IncidentStyle
import json, textwrap, argparse
import yaml

argParser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
argParser.add_argument("-c", "--config", help=" The config file")
argParser.add_argument('action', metavar='action', choices=['small_power', 'medium_power', 'large_power', 'power_returned'],
                    help=textwrap.dedent('''\
                    The action you wish to perform.
                    Supported actions are:
                     - small_power - the beggining of a power outage
                     - medium_power - the power outage has proceeded longer than expected
                     - large_power - The power has been out too long and the server will soon shutdown
                     - power_returned - the end of a power outage'
                    '''))

args = argParser.parse_args()

# Load a YAML file
with open(args.config) as f:
  config = yaml.safe_load(f)

print(config)
print(args.action)
if False:
    with UptimeKumaApi(config['url']) as api:
        api.login(config['login']['username'], config['login']['password'])
        statuspagecurrent = api.get_status_page("main")
        print(statuspagecurrent)
        if statuspagecurrent['incident'] == None:
            api.post_incident(
                slug="main",
                title="title 1",
                content="content 1",
                style=IncidentStyle.DANGER
            )