from pathlib import Path

import xml.etree.ElementTree as ET
import classes.globals as g
import classes.functions as func


class Query(object):
    def __init__(self, filename, query_type):
        self.filename = filename
        self.query_type = query_type
        self.register_namespaces()

    def register_namespaces(self):
        self.namespaces = {
            'ns2': 'http://www.eurodyn.com/Tariff/services/DispatchDataExportXMLData/v03'
        }
        self.namespaces = {}
        for ns in self.namespaces:
            ET.register_namespace(ns, self.namespaces[ns])

    def run_query(self):
        if self.query_type == "quotas":
            ret, exclusions = self.run_query_quotas()

        return (ret, exclusions)

    def run_query_quotas(self):
        ret = []
        exclusions = []
        root = ET.parse(self.filename)
        self.query = ".//QuotaOrderNumber"
        for elem in root.findall(self.query, self.namespaces):
            quota_order_number_id = self.get_value(elem, "quotaOrderNumberId")
            if quota_order_number_id.startswith("05"):
                obj = {}
                obj["hjid"] = int(self.get_value(elem, "hjid"))
                obj["operation_type"] = self.get_value(elem, "metainfo/opType")
                obj["transaction_date"] = self.get_value(elem, "metainfo/transactionDate")
                obj["quota_order_number_id"] = quota_order_number_id
                obj["quota_order_number_sid"] = int(self.get_value(elem, "sid"))
                obj["validity_start_date"] = self.get_value(elem, "validityStartDate")
                obj["validity_end_date"] = self.get_value(elem, "validityEndDate")
                obj["quota_order_number_origins"] = []
                obj["filename"] = Path(self.filename).stem
                origin_count = 0
                for origin in elem.findall(".//quotaOrderNumberOrigin", self.namespaces):
                    origin_count += 1
                    origin_obj = {}
                    origin_obj["hjid"] = int(self.get_value(origin, "hjid"))
                    origin_obj["sid"] = int(self.get_value(origin, "sid"))
                    origin_obj["geographical_area_sid"] = int(self.get_value(origin, "geographicalArea/sid"))
                    origin_obj["geographical_area_id"] = self.get_value(origin, "geographicalArea/geographicalAreaId")
                    origin_obj["validity_start_date"] = str(self.get_value(origin, "geographicalArea/validityStartDate"))
                    origin_obj["validity_end_date"] = str(self.get_value(origin, "geographicalArea/validityEndDate"))
                    origin_obj["exclusions"] = []

                    for exclusion in origin.findall(".//quotaOrderNumberOriginExclusions", self.namespaces):
                        exclusion_obj = {}
                        exclusion_obj["quota_order_number_id"] = obj["quota_order_number_id"]
                        exclusion_obj["quota_order_number_sid"] = obj["quota_order_number_sid"]
                        exclusion_obj["quota_order_number_origin_sid"] = origin_obj["sid"]
                        exclusion_obj["hjid"] = int(self.get_value(exclusion, "hjid"))
                        exclusion_obj["excluded_geographical_area_sid"] = int(self.get_value(exclusion, "geographicalArea/sid"))
                        exclusion_obj["excluded_geographical_area_id"] = self.get_value(exclusion, "geographicalArea/geographicalAreaId")
                        exclusion_obj["country"] = g.countries[exclusion_obj["excluded_geographical_area_id"]]
                        filename_parts = func.get_filename_parts(self.filename)
                        exclusion_obj["filename"] = filename_parts[0]
                        exclusion_obj["operation_date"] = filename_parts[1]
                        origin_obj["exclusions"].append(exclusion_obj)
                        exclusions.append(exclusion_obj)
                        a = 1

                    obj["quota_order_number_origins"].append(origin_obj)
                    a = 1

                obj["origin_count"] = origin_count
                ret.append(obj)

        if len(ret) == 0:
            ret = None

        return (ret, exclusions)

    def get_value(self, elem, query):
        obj = elem.find(query, self.namespaces)
        if obj is None:
            return ""
        else:
            return obj.text
