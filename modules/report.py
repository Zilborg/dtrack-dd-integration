# defect Dojo parser for DTrack:
# https://github.com/DefectDojo/django-DefectDojo/blob/master/dojo/tools/dependency_track/parser.py

"""
    A class that can be used to parse the JSON Finding Packaging Format (FPF) export from OWASP Dependency Track.
    See here for moe info on this JSON format: https://docs.dependencytrack.org/integrations/file-formats/
    A typical Finding Packaging Format (FPF) export looks like the following:
    {
        "version": "1.0",
        "meta" : {
            "application": "Dependency-Track",
            "version": "3.4.0",
            "timestamp": "2018-11-18T23:31:42Z",
            "baseUrl": "http://dtrack.example.org"
        },
        "project" : {
            "uuid": "ca4f2da9-0fad-4a13-92d7-f627f3168a56",
            "name": "Acme Example",
            "version": "1.0",
            "description": "A sample application" 
        },
        "findings" : [
            {
                "component": {
                    "uuid": "b815b581-fec1-4374-a871-68862a8f8d52",
                    "name": "timespan",
                    "version": "2.3.0",
                    "purl": "pkg:npm/timespan@2.3.0"
                },
                "vulnerability": {
                    "uuid": "115b80bb-46c4-41d1-9f10-8a175d4abb46",
                    "source": "NPM",
                    "vulnId": "533",
                    "title": "Regular Expression Denial of Service",
                    "subtitle": "timespan",
                    "severity": "LOW",
                    "severityRank": 3,
                    "cweId": 400,
                    "cweName": "Uncontrolled Resource Consumption ('Resource Exhaustion')",
                    "description": "Affected versions of `timespan`...",
                    "recommendation": "No direct patch is available..."
                },
                "analysis": {
                    "state": "NOT_SET",
                    "isSuppressed": false
                },
                "matrix": "ca4f2da9-0fad-4a13-92d7-f627f3168a56:b815b581-fec1-4374-a871-68862a8f8d52:115b80bb-46c4-41d1-9f10-8a175d4abb46"
            },
            {
                "component": {
                    "uuid": "979f87f5-eaf5-4095-9d38-cde17bf9228e",
                    "name": "uglify-js",
                    "version": "2.4.24",
                    "purl": "pkg:npm/uglify-js@2.4.24"
                },
                "vulnerability": {
                    "uuid": "701a3953-666b-4b7a-96ca-e1e6a3e1def3",
                    "source": "NPM",
                    "vulnId": "48",
                    "title": "Regular Expression Denial of Service",
                    "subtitle": "uglify-js",
                    "severity": "LOW",
                    "severityRank": 3,
                    "cweId": 400,
                    "cweName": "Uncontrolled Resource Consumption ('Resource Exhaustion')",
                    "description": "Versions of `uglify-js` prior to...",
                    "recommendation": "Update to version 2.6.0 or later."
                },
                "analysis": {
                    "isSuppressed": false
                },
                "matrix": "ca4f2da9-0fad-4a13-92d7-f627f3168a56:979f87f5-eaf5-4095-9d38-cde17bf9228e:701a3953-666b-4b7a-96ca-e1e6a3e1def3"
            }]
    }
"""


# Need only findings 
# Exclude component.uuid, vulnerability.(severityRank, cweName), matrix
def prepare_json(cols, records):
    findings_by_productID = {}
    findings = []
    for record in records:
        project_name = record[cols.index('NAME')]
        project_name_ind = cols.index('NAME')
        lib_name = record[cols.index('NAME', project_name_ind+1)]

        component = {
            "name": '{}:{}'.format(project_name,lib_name),
            "version": record[cols.index('VERSION')],
            "purl": record[cols.index('PURL')],
        }
        vulnerability = {
            "uuid": record[cols.index('UUID')],
            "source": record[cols.index('SOURCE')],
            "vulnId": record[cols.index('VULNID')],
            "title": record[cols.index('TITLE')],
            "subtitle": record[cols.index('SUBTITLE')],
            "severity": record[cols.index('SEVERITY')],
            "cweId": record[cols.index('CWE')],
            "description":record[cols.index('DESCRIPTION')],
            "recommendation": record[cols.index('RECOMMENDATION')]
        }
        analysis = None

        findings.append({
            "component": component,
            "vulnerability": vulnerability,
            "analysis": analysis
        })
        prop = record[cols.index('PROPERTYVALUE')]
        if prop in findings_by_productID:
            findings_by_productID[prop]["findings"].append(findings)
        else:
            findings_by_productID.update({
                prop: {
                    "version": "1.0",
                    "meta" : {
                        "application": "Dependency-Track",
                        "version": "",
                        "timestamp": "",
                        "baseUrl": ""
                    },
                    "project" : {
                        "uuid": "",
                        "name": "",
                        "version": "",
                        "description": "" 
                    },
                    "findings": findings
                }
            })
    return findings_by_productID