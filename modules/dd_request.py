import requests
import os
import datetime
import json

TOKEN = os.environ.get('DD_TOKEN')
DD_HOST= os.environ.get('DD_HOST')
PROGRES_DAYS = int(os.environ.get('PROGRES_DAYS', '5'))

headers = {
    'Authorization': 'Token {}'.format(TOKEN)
}

def dd_create_engagements(product_id):
    headers_ = headers.copy()
    headers_.update({
        'Content-Type': 'application/json'
    })

    dd_create_engagement_ = {
        "target_start": datetime.datetime.now().strftime("%Y-%m-%d"),
        "target_end": (datetime.datetime.now() + datetime.timedelta(days=PROGRES_DAYS)).strftime("%Y-%m-%d"),
        "product": int(product_id),
        "tags": [
            "dtrack",
        ],
        "name": "Dependency Track",
        "description": "",
        # "version": None,
        "first_contacted": datetime.datetime.now().strftime("%Y-%m-%d"),
        "reason": "string",
        "threat_model": False,
        "api_test": True,
        "pen_test": True,
        "check_list": True,
        "status": "Not Started",
        "engagement_type": "CI/CD",
        # "build_id": None,
        # "commit_hash": None,
        # "branch_tag": None,
        "deduplication_on_engagement": False
    }
    r = requests.post('{}/engagements/'.format(DD_HOST), data=json.dumps(dd_create_engagement_), headers=headers_)
    if r.status_code == 201:
        engagement_id = r.json()['id']
        return engagement_id
    else:
        return None


def dd_import(engagement_id, report_data):
    dd_import = {
        'scan_type': 'Dependency Track Finding Packaging Format (FPF) Export',
        'engagement': int(engagement_id),
        'scan_date': datetime.datetime.now().strftime("%Y-%m-%d"),
        'minimum_severity': 'Info',
        'active': 'true',
        'verified': 'true',
        'close_old_findings': 'false',
        'push_to_jira': 'false',
        'environment': 'Default',
    }
    upload_file = {'file':  report_data.encode()}
    # upload_file.update(dd_import)
    r = requests.post('{}/import-scan/'.format(DD_HOST), headers=headers,
                        data=dd_import,files=upload_file
                    )
    print(r.request.headers)
    print(r.request.body)
    print(r.text)
    if r.status_code == 201:
        return r.status_code
    
    