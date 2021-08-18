# Get vulns to sync
temp1 = 'select * from "ANALYSIS" INNER JOIN "VULNERABILITY" ON "ANALYSIS"."VULNERABILITY_ID" = "VULNERABILITY"."ID"  where "ANALYSIS"."STATE" in (\'EXPLOITABLE\', \'IN_TRIAGE\');'


# Get vulns to sync with properties
ex_get_vulns_to_sync='''
select * from "ANALYSIS" inner join "VULNERABILITY" 
on "ANALYSIS"."VULNERABILITY_ID" = "VULNERABILITY"."ID" inner join 
    (select "PROJECT_ID","NAME","GROUPNAME","PROPERTYNAME","PROPERTYTYPE","PROPERTYVALUE" from "PROJECT" 
        INNER JOIN "PROJECT_PROPERTY" ON "PROJECT"."ID"="PROJECT_PROPERTY"."PROJECT_ID" 
        where "GROUPNAME" = 'integrations' and "PROPERTYNAME" = 'defectdojo.productid'
    ) as prop on prop."PROJECT_ID"="ANALYSIS"."PROJECT_ID" inner join 
    (select "ID","NAME","VERSION","PURL" from "COMPONENT"
    ) as comp on comp."ID" = "ANALYSIS"."COMPONENT_ID"
where "ANALYSIS"."STATE" = 'EXPLOITABLE';
'''

# Set indicator that vuln sent
def update_triage(id):
  return '''
  update "ANALYSIS" SET "STATE" = '{}' where "ID" = '{}'
  '''.format('IN_TRIAGE', id)

# Add commnet
def add_comment(id):
  return '''
  insert into "ANALYSISCOMMENT"("ANALYSIS_ID", "COMMENT", "COMMENTER", "TIMESTAMP") values ({}, '{}', '{}', %s)
  '''.format(int(id), 'EXPLOITABLE → IN_TRIAGE', 'sync')