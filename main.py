from datetime import datetime
import psycopg2
from psycopg2 import Error
import logging
import os
import json
import datetime

from modules.logs import init_log
from modules.db import ex_get_vulns_to_sync, update_triage, add_comment
from modules.report import prepare_json
from modules.dd_request import dd_create_engagements, dd_import

user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
db_host = os.environ.get('DB_HOST')
database = os.environ.get('POSTGRES_USER')
log_level = os.environ.get("LOGLEVEL", "INFO")

## OTHER VARIABLES
# TOKEN = os.environ.get('DD_TOKEN')
# DD_HOST= os.environ.get('DD_HOST')
# PROGRES_DAYS = int(os.environ.get('PROGRES_DAYS', '5'))

init_log(log_level)

def main():
    conn = None
    try:
        conn = psycopg2.connect(dbname=database, user=user, 
                                password=password, host=db_host)
        cursor = conn.cursor()
        cursor.execute(ex_get_vulns_to_sync)
        records = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        logging.debug(colnames)
        logging.debug(records)
        data_by_id = prepare_json(colnames, records)
        for product_id in data_by_id.keys():
            engagement_id = dd_create_engagements(product_id)
            if engagement_id:
                logging.info("Engagement id {}".format(engagement_id))
                resp_code = dd_import(engagement_id, json.dumps(data_by_id[product_id]))
                if resp_code == 201:
                    logging.info("Data was imported")
                    for record in records:
                        cursor.execute(update_triage(record[0]))
                        cursor.execute(add_comment(record[0]), (datetime.datetime.now(),))
                        conn.commit()
                        logging.debug("Updated ANALYSIS: {}".format(record[0]))
                    logging.info("Records updated")
                else:
                    logging.error("Cannot import")
            else:
                logging.error("Cannot create engagement")
                exit(1)

    except (Exception, Error) as error:
         logging.exception("Exception in main(): ")
         exit(1)
    finally:
        if conn:
            logging.info("Connection close")
            cursor.close()
            conn.close()


if __name__ == "__main__":
    main()