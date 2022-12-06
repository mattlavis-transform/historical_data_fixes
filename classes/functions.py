import re
import os
import classes.globals as g


def get_paths():
    g.resource_path = os.path.join(os.getcwd(), "resources")
    g.quota_order_number_origins_path = os.path.join(g.resource_path, "quota_order_number_origins")
    a = 1

def date_to_json(d):
    if d is None:
        return None
    else:
        return str(d)

def get_filename_parts(xml_filename):
    if "/" in xml_filename:
        parts = xml_filename.split("/")
        xml_filename = parts[-1]
    xml_filename = xml_filename.replace("-", "_")
    parts = xml_filename.split("_")
    gzip_filename = "tariff_dailyExtract_v1_{placeholder}.gzip".format(placeholder=parts[2])
    operation_date = parts[1]
    operation_date = operation_date[0:4] + "-" + operation_date[4:6] + "-" + operation_date[6:8]
    ret = (
        gzip_filename,
        operation_date
    )
    return ret

def get_migration_script(obj, filename):
    filename_parts = get_filename_parts(filename)
    obj["filename"] = filename_parts[0]
    obj["operation_date"] = filename_parts[1]
    if obj["validity_end_date"] is None:
        validity_end_date = 'null'
    else:
        validity_end_date = "'" + obj["validity_end_date"] + "'"

    obj["operation_date"] = '2022-01-01'
    migration_string = """
    insert into quota_order_number_origins
    (
        quota_order_number_origin_sid,
        quota_order_number_sid,
        geographical_area_id,
        validity_start_date,
        validity_end_date,
        geographical_area_sid,
        operation,
        operation_date,
        filename
    )
    values (
        {quota_order_number_origin_sid},
        {quota_order_number_sid},
        '{geographical_area_id}',
        '{validity_start_date}',
        {validity_end_date},
        {geographical_area_sid},
        '{operation}',
        '{operation_date}',
        '{filename}'
    );
    """.format(
        quota_order_number_origin_sid=obj["quota_order_number_origin_sid"],
        quota_order_number_sid=obj["quota_order_number_sid"],
        geographical_area_id=obj["geographical_area_id"],
        validity_start_date=obj["validity_start_date"],
        validity_end_date=validity_end_date,
        geographical_area_sid=obj["geographical_area_sid"],
        operation="D",
        operation_date=obj["operation_date"],
        filename=obj["filename"],
    ).replace("\n", " ")

    migration_string = re.sub("\s+", " ", migration_string).strip()
    migration_string = migration_string.replace("( ", "(")
    migration_string = migration_string.replace(" )", ")")
    return migration_string
