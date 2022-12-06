import os
import re
import sys
import csv
import json
import glob
from dotenv import load_dotenv

from classes.query import Query
from classes.database import Database
import classes.functions as func
import classes.globals as g

func.get_paths()
# Get countries
d = Database()
sql = "select geographical_area_id, description from utils.geographical_areas ga order by 1;"
params = []
countries = d.run_query(sql, params)
for country in countries:
    g.countries[country[0]] = country[1]

load_dotenv('.env')
folder = os.getenv('CDS_DATA_FOLDER')

files = glob.glob(folder + '/*.xml')
files = sorted(files, reverse=True)
records = []
exclusions = []
max_count = 200000
count = 0
for filename in files:
    count += 1
    print(filename)
    q = Query(filename, "quotas")
    ret, quota_exclusions = q.run_query()

    # Origins
    if ret is not None:
        records += ret

    # Exclusions
    dealt_with = []
    if len(quota_exclusions) > 0:
        for quota_exclusion in quota_exclusions:
            compound_key = str(quota_exclusion["quota_order_number_origin_sid"]) + "_" + str(quota_exclusion["excluded_geographical_area_sid"])
            if compound_key not in dealt_with:
                exclusions.append(quota_exclusion)
                dealt_with.append(compound_key)

    # Stop if you hit the max
    if count > max_count:
        break

# Write the exclusions CSV
if len(exclusions) > 0:
    exclusions_csv_path = os.path.join(g.quota_order_number_origins_path, 'quota_order_number_origin_exclusions.csv')
    exclusions_sql_path = os.path.join(g.quota_order_number_origins_path, 'quota_order_number_origin_exclusion_migrations.sql')
    csv_file = open(exclusions_csv_path, 'w')
    sql_file = open(exclusions_sql_path, 'w')
    writer = csv.writer(csv_file)
    writer.writerow(['quota_order_number_id', 'quota_order_number_sid', 'quota_order_number_origin_sid', 'hjid', 'excluded_geographical_area_sid', 'excluded_geographical_area_id', 'country', 'filename', 'operation_date'])
    for exclusion in exclusions:
        writer.writerow(exclusion.values())
        sql_line = """
        insert into quota_order_number_origin_exclusions_oplog
        (quota_order_number_origin_sid, excluded_geographical_area_sid, operation, operation_date, filename, created_at)
        values
        ({quota_order_number_origin_sid}, {excluded_geographical_area_sid}, '{operation}', '{operation_date}', '{filename}', '{created_at}');
        """.format(
            quota_order_number_origin_sid=exclusion["quota_order_number_origin_sid"],
            excluded_geographical_area_sid=exclusion["excluded_geographical_area_sid"],
            operation="C",
            operation_date=exclusion["operation_date"],
            filename=exclusion["filename"],
            created_at=exclusion["operation_date"]
        ).replace("\n", " ").strip()
        sql_line = re.sub("\s+", " ", sql_line)
        sql_file.write(sql_line + "\n")
    csv_file.close()
    sql_file.close()

records = sorted(records, key=lambda x: x["transaction_date"], reverse=True)
records = sorted(records, key=lambda x: x["quota_order_number_id"], reverse=False)

json_path = os.path.join(g.quota_order_number_origins_path, 'data.json')
with open(json_path, 'w') as f:
    json.dump(records, f, indent=4)

csv_path = os.path.join(g.quota_order_number_origins_path, 'data.csv')
f = open(csv_path, 'w')
for record in records:
    origins = []
    for quota_order_number_origin in record["quota_order_number_origins"]:
        origins.append(quota_order_number_origin["geographical_area_id"])
    f.write('"' + record["transaction_date"] + '", ')
    f.write('"' + record["quota_order_number_id"] + '", ')
    f.write('"' + "|".join(origins) + '"\n')

f.close()

dealt_with = []
mismatches = []
all_migrations = []
for record in records:
    quota_order_number_sid = record["quota_order_number_sid"]
    if quota_order_number_sid not in dealt_with:
        # Get the quota order number origin exclusions for this quota
        d = Database()
        sql = """
        select qonoe.* from quota_order_number_origins qono, quota_order_number_origin_exclusions qonoe
        where qono.quota_order_number_origin_sid = qonoe.quota_order_number_origin_sid
        and quota_order_number_sid = %s"""
        params = [quota_order_number_sid]
        exclusions = d.run_query(sql, params)

        # Get the quota order number origins for this quota
        d = Database()
        sql = """select geographical_area_id, validity_start_date, validity_end_date,
        quota_order_number_origin_sid, quota_order_number_sid, geographical_area_sid
        from quota_order_number_origins where quota_order_number_sid = %s"""

        params = [quota_order_number_sid]
        rows = d.run_query(sql, params)
        database_origins = []
        database_origins2 = []
        for row in rows:
            if len(exclusions) > 0:
                a = 1
            database_origins.append(row[0])
            database_obj = {
                "geographical_area_id": row[0],
                "validity_start_date": func.date_to_json(row[1]),
                "validity_end_date": func.date_to_json(row[2]),
                "quota_order_number_origin_sid": row[3],
                "quota_order_number_sid": row[4],
                "geographical_area_sid": row[5]
            }
            database_origins2.append(database_obj)

        file_origins = []
        file_origins2 = []
        for origin in record["quota_order_number_origins"]:
            file_origins.append(origin["geographical_area_id"])
            file_obj = {
                "geographical_area_id": origin["geographical_area_id"],
                "validity_start_date": func.date_to_json(origin["validity_start_date"]),
                "validity_end_date": func.date_to_json(origin["validity_end_date"])
            }
            file_origins2.append(file_obj)

        file_origins.sort()
        migrations = []
        database_origins.sort()
        if file_origins != database_origins:
            if len(database_origins) > len(file_origins):
                for database_origin in database_origins2:
                    a = 1
                    if database_origin["geographical_area_id"] not in file_origins:
                        migration = func.get_migration_script(database_origin, record["filename"])
                        migrations.append(migration)
                        all_migrations.append(migration)

            mismatch_obj = {
                "quota_order_number_sid": record["quota_order_number_sid"],
                "quota_order_number_id": record["quota_order_number_id"],
                "database_origins": database_origins2,
                "file_origins": file_origins2,
                "latest_update_xml": record["filename"],
                "migrations": migrations
            }
            mismatches.append(mismatch_obj)

    dealt_with.append(quota_order_number_sid)

if len(dealt_with) > 0:
    quota_mismatches_json_path = os.path.join(g.quota_order_number_origins_path, 'quota_mismatches.json')
    with open(quota_mismatches_json_path, 'w') as f:
        json.dump(mismatches, f, indent=4)

quota_mismatches_csv_path = os.path.join(g.quota_order_number_origins_path, 'quota_order_number_origin_migrations.sql')
f = open(quota_mismatches_csv_path, 'w')
for migration in all_migrations:
    f.write(migration + "\n")
