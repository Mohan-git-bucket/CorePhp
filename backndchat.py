from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

backend_data = {
    "remote stm for US": "ssh 10.12.3.150 DB  remote_stm_aws.",
    "remote stm for IND": "server remote-stm-prod-ind.netcorein.com {10.15.1.101}",
    "storm logs for US idc from s3": (
        'for j in {01..06}; do for i in {06..07}; do for k in {00..23}; do echo "-----"; '
        'aws s3 cp s3://storm2x-backup/stsup-$j/202503$i$k . --recursive --exclude "*" --include "cg2*"; '
        'done; done; done;\n'
        '--j is machine server\n'
        '--i is the date that need to be change\n'
        '--k is hours'
    ),
    "storm for tata idc from s3": (
        'for j in {01..05}; do for i in {01..02}; do echo "-----"; '
        'aws s3 cp s3://stsup-backup/stsup-$j/202308$i . --recursive --exclude "*" --include "cg03*"; '
        'done; done;'
    ),
    "storm log for EU IDC s3": (
        'aws s3 cp s3://backup-smartech-eu-logs/storm-supervisor/20240126/ . --recursive --exclude "" --include "cg2"'
    ),
    "Live storm machine for IND idc": (
        'jumpcloud\n'
        'stsup-01-in.netcorein.com\n'
        'stsup-02-in.netcorein.com\n'
        'stsup-03-in.netcorein.com\n'
        'stsup-04-in.netcorein.com\n'
        'stsup-05-in.netcorein.com\n'
        'Logs path: /var/log/apps/storm2x/\n'
    ),
    "Live storm machine for US idc": (
        'jumpcloud-us\n'
        'ssh stsup-01-us.netcorein.com\n'
        'ssh stsup-02-us.netcorein.com\n'
        'ssh stsup-03-us.netcorein.com\n'
        'ssh stsup-04-us.netcorein.com\n'
        'ssh stsup-05-us.netcorein.com\n'
        'ssh stsup-06-us.netcorein.com\n'
        'Logs path: /var/log/apps/storm2x/\n'
    ),
    "Live storm machine for EU idc": (
        'jump-euro\n'
        'ssh 10.106.2.187\n'
        'ssh 10.106.2.89\n'
        'Logs path: /var/log/apps/storm2x/\n'
    ),
    "papi dequeue logs for US from s3": ('\n'
        'aws s3 cp s3://nc-serverbackup-us/activity-papi-deq-01/papi_dequeue/2024-01-10/ . --recursive'
    ),
    "papi dequeue logs for IND from s3": ('\n'
        'aws s3://nc-serverbackup-mu/activity-papi-deq-01/papi_dequeue/$date1'
    ),
    "Live papi dequeue machine for US idc": ('\n'
        'activity-papi-deq-01 ==> 10.12.13.55\n'
        'activity-papi-deq-02 ==> 10.12.13.221\n'
        'activity-papi-deq-03 ==> 10.12.13.112\n'
        'activity-papi-deq-04 ==> 10.12.13.93\n'
        'activity-papi-deq-05 ==> 10.12.13.165\n'
        'Path to the machine: /var/log/'
    ),
    "Live papi dequeue machine for IND idc": ('\n'
        'activity-papi-dequeuer-01-prod-ind => 10.15.1.229\n'
        'activity-papi-dequeuer-02-prod-ind => 10.15.1.24\n'
        'activity-papi-dequeuer-03-prod-ind => 10.15.1.70'
    ),
    "Live papi dequeue machine for EU idc": (
        'ssh -i eu-platform-papi.pem centos@activity-papi.eu-north-1.eu.smt.internal => 10.106.0.236\n'
    ),
    "App Lambda name server": ('\n'
        'smtfluentd-01-prod-ind ==> 10.15.1.104\n'
        'smtfluentd-02-prod-ind ==> 10.15.1.216\n'
        'smtfluentd-03-prod-ind ==> 10.15.1.142\n'
        'smtfluentd-04-prod-ind ==> 10.15.1.191\n'
        'smtfluentd-05-prod-ind ==> 10.15.1.106\n'
        'smtfluentd-06-prod-ind ==> 10.15.1.168\n'
        'smtfluentd-prod-ind ==> 10.15.1.188\n'
        'smtredis-prod-ind ==> 10.15.1.149\n'
        'Path to the machine: /var/log/fluent'
),
    "To download app lambda logs from s3 (backup)": ('\n'
        '1) aws s3 sync --profile sysbackup --exclude="*" --include="twlogs.20250523*" '
        's3://nc-serverbackup-mu/ip-10-15-1-104.ap-south-1.compute.internal/var/log/fluent/20250523 .\n'
        '2) aws s3 sync --profile sysbackup --exclude="*" --include="twlogs.20250523*" '
        's3://nc-serverbackup-mu/ip-10-15-1-216.ap-south-1.compute.internal/var/log/fluent/20250523 .\n'
        '3) aws s3 sync --profile sysbackup --exclude="*" --include="twlogs.20250523*" '
        's3://nc-serverbackup-mu/ip-10-15-1-142.ap-south-1.compute.internal/var/log/fluent/20250523 .\n'
        '4) aws s3 sync --profile sysbackup --exclude="*" --include="twlogs.20250523*" '
        's3://nc-serverbackup-mu/ip-10-15-1-191.ap-south-1.compute.internal/var/log/fluent/20250523 .\n'
        '5) aws s3 sync --profile sysbackup --exclude="*" --include="twlogs.20250523*" '
        's3://nc-serverbackup-mu/ip-10-15-1-106.ap-south-1.compute.internal/var/log/fluent/20250523 .\n'
        '6) aws s3 sync --profile sysbackup --exclude="*" --include="twlogs.20250523*" '
        's3://nc-serverbackup-mu/ip-10-15-1-168.ap-south-1.compute.internal/var/log/fluent/20250523 .\n'
        '7) aws s3 sync --profile sysbackup --exclude="*" --include="twlogs.20250523*" '
        's3://nc-serverbackup-mu/ip-10-15-1-149.ap-south-1.compute.internal/var/log/fluent/20250523 .'
    ),
    "Kibana/Cibana Dashboards": ('\n'
        '<a href="http://clkibana.netcore.co.in:5601/" target="_blank">US Kibana Dashboard</a>\n'
        '<a href="https://clkibana-ind.netcorein.com/" target="_blank">IND Kibana Dashboard</a>\n'
        '<a href="http://clkibana-eu.netcore.co.in:5601/" target="_blank">EU Kibana Dashboard</a>\n'
        '\n'
        '<strong>User:</strong> devops\n'
        '<strong>Password:</strong> Sm@rtL0gVu82'
    ),
    "EL logs / Event Logger for US from s3": ('\n'
        'aws s3 cp s3://netcore-central-logging-backup/central-logging/prod-us/event-logger/2024/11/06/10/ . --recursive'
    ),
    "EL logs / Event Logger for IND from s3 ": ('\n'
        'aws s3 cp s3://netcore-central-logging-backup-ind/central-logging/prod-ind/event-logger/2023/01/03/ . --recursive'
    ),
    "S2S Offline Web Live Server": ('\n'
        'smtfluentd-01-prod-ind.netcorein.com\n'
        'smtfluentd-06-prod-ind.netcorein.com\n\n'
        's3 command to download the log from s3:\n'
        '1) nohup aws s3 sync --profile sysbackup --exclude="*" --include="offlineweb.2025052*" '
        's3://nc-serverbackup-mu/ip-10-15-1-168.ap-south-1.compute.internal/var/log/fluent/ . &\n'
        '2) nohup aws s3 sync --profile sysbackup --exclude="*" --include="offlineweb.2025052*" '
        's3://nc-serverbackup-mu/ip-10-15-1-104.ap-south-1.compute.internal/var/log/fluent/ . &'
    ),
    "Vertica-SmartAnalytics Logs for US-idc": ('\n'
    'port1 --> ssh 3.231.35.132\n'
    '└── ssh 172.30.129.6\n'
    '└── ssh 172.30.129.162'
    ),
    "Vertica-SmartAnalytics Logs For IND-idc": ('\n'
        'jumprivate\n'
        'ssh 172.31.82.78\n'
        'ssh 172.31.82.100'
    ),
    "Journey Basic": (
    'To grep how many times a journey is deployed through Audit logs:\n'
    'zgrep \'"journey saved successfully.","data":{"id":"140"}\' audit_log.log*\n\n'

    'To check how many times journey deployed through subsapi machine:\n'
    'cloud =>\n'
    '  (for IND IDC) subsapi-02-us.netcorein.com\n'
    '  (for US IDC)\n'
    'zgrep "184039.155" /var/log/apps/subsapi2/subsapi.log /var/log/apps/subsapi2/subsapi.log_2025* | grep "inside nmi_lambda with status"\n'
    '========== clientid.automation_id\n\n'

    'To check dataset automation last executed time at papi db (IND/US):\n'
    'cloud => papi-db-prod-ind.netcorein.com (for IND)\n'
    'select * from papi_automation_dataset where cid=182495 and aid=30\\G;\n'
    'refer value of prev_exec_time\n\n'

    'cg00: Users coming out of wait for activity\n'
    'cg01: Activity Based Journey\n'
    'cg02: Users coming out of wait for dataset / S2S offline activity\n'
    'cg03: Dataset Journey\n\n'

    'To look for any activity in storm logs, it is advisable to look via guid of the user (get guid from vertica)\n'
    'Then in the output logs look for the following pattern:\n'
    '179490,101,4,  (clientid, activityid, userid)'
),





}

def search_backend(query):
    results = []
    for key, value in backend_data.items():
        if query.lower() in key.lower():
            results.append(f"{key.title()}: {value}")
    return results

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    results = search_backend(query)
    return jsonify(results=results)

@app.route('/')
def index():
    return send_from_directory('.', 'chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)