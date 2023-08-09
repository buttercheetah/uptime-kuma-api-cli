from uptime_kuma_api import UptimeKumaApi, MonitorType, IncidentStyle
import json, textwrap, argparse, os, yaml

argParser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
argParser.add_argument("config_file", type=str, help="The config file")
argParser.add_argument('action', metavar='action', choices=['small_power', 'medium_power', 'large_power', 'power_returned','clear'],
                    help=textwrap.dedent('''\
                    The action you wish to perform.
                    Supported actions are:
                     - small_power - the beggining of a power outage
                     - medium_power - the power outage has proceeded longer than expected
                     - large_power - The power has been out too long and the server will soon shutdown
                     - power_returned - the end of a power outage
                     - clear - Removes pinned incident from UptimeKuma
                    '''))
argParser.add_argument('slug', metavar='slug', type=str, help='The slug of the page you wish to modify.')

args = argParser.parse_args()


if not os.path.isfile('template.yaml'):
    print("template.yaml not found! Please Read the README!")
    exit(1)

# Load a YAML file
with open(args.config_file) as f:
  config = yaml.safe_load(f)


def ClearIncident(slug):
    with UptimeKumaApi(config['url']) as api:
        api.login(config['login']['username'], config['login']['password'])
        statuspagecurrent = api.get_status_page(slug)
        if statuspagecurrent['incident'] == None:
            print("There is no current incident")
        else:
            print("Unpining current incident")
            api.unpin_incident(slug=slug)

def GetStatusPages():
    with UptimeKumaApi(config['url']) as api:
        api.login(config['login']['username'], config['login']['password'])
        return api.get_status_pages()

def VerifySlug(slug):
    pages = GetStatusPages()
    for i in pages:
        if i['slug'] == slug:
            return True
    return False

def GetIncidentStyle(style):
    # Options for style:
    # INFO,WARNING,DANGER,PRIMARY,LIGHT,DARK
    if style.upper() == 'INFO': return IncidentStyle.INFO
    if style.upper() == 'WARNING': return IncidentStyle.WARNING
    if style.upper() == 'DANGER': return IncidentStyle.DANGER
    if style.upper() == 'PRIMARY': return IncidentStyle.PRIMARY
    if style.upper() == 'LIGHT': return IncidentStyle.LIGHT
    if style.upper() == 'DARK': return IncidentStyle.DARK

def CreateIncident(slug, kind, overwrite=False):
    with open('template.yaml') as f:
        template = yaml.safe_load(f)
        #print(template)
    if not VerifySlug(slug):
        print("The slug cannot be found!")
        exit(1)
    with UptimeKumaApi(config['url']) as api:
        api.login(config['login']['username'], config['login']['password'])
        statuspagecurrent = api.get_status_page(slug)
        if statuspagecurrent['incident'] != None:
            if overwrite == False:
                print("There is already an incident found!\nOverwrite is not enabled!")
                exit(1)
            else:
                ClearIncident(slug)
        api.post_incident(
            slug=slug,
            title=template[kind]['title'],
            content=template[kind]['desc'],
            style=GetIncidentStyle(template[kind]['style'])
        )
        print("Posting new incident")

if args.action == 'clear':
    ClearIncident(args.slug)
else:
    CreateIncident(args.slug, args.action, True)