import os
import xml.etree.ElementTree as ET
from pathlib import Path
import classes.functions as f


class XpathQueryCds(object):
    def __init__(self, filename, query_class, query_id, scope):
        self.filename = filename
        self.query_class = query_class
        self.query_id = query_id
        self.scope = scope
        self.register_namespaces()

    def register_namespaces(self):
        self.namespaces = {
            'ns2': 'http://www.eurodyn.com/Tariff/services/DispatchDataExportXMLData/v03'
        }
        self.namespaces = {}
        for ns in self.namespaces:
            ET.register_namespace(ns, self.namespaces[ns])

    def run_query_measure(self, root):
        ret = []
        self.query = ".//Measure[sid = '{item}']".format(item=self.query_id)
        for elem in root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            goods_nomenclature_sid = self.get_value(elem, "goodsNomenclature/sid")
            goods_nomenclature_item_id = self.get_value(elem, "goodsNomenclature/goodsNomenclatureItemId")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            measure_type_id = self.get_value(elem, "measureType/measureTypeId")
            geographical_area_id = self.get_value(elem, "geographicalArea/geographicalAreaId")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, goods_nomenclature_item_id, validity_start_date,
                   validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def run_query_measure_condition(self, root):
        ret = []
        self.query = ".//measureCondition[sid = '{item}']/..".format(item=self.query_id)
        for elem in root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            measure_sid = self.get_value(elem, "sid")
            measure_condition_code = self.get_value(elem, "measureCondition/measureConditionCode/conditionCode")
            component_sequence_number = self.get_value(elem, "measureCondition/conditionSequenceNumber")
            action_code = self.get_value(elem, "measureCondition/measureAction/actionCode")
            certificate_type_code = self.get_value(elem, "measureCondition/certificate/certificateType/certificateTypeCode")
            certificate_code = self.get_value(elem, "measureCondition/certificate/certificateCode")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, measure_sid, measure_condition_code, component_sequence_number, action_code, certificate_type_code, certificate_code)
            ret.append(obj)
        return ret

    def run_query_commodity(self, root):
        ret = []
        self.query = ".//GoodsNomenclature[goodsNomenclatureItemId = '{item}']".format(
            item=self.query_id)
        for elem in root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            sid = self.get_value(elem, "sid")
            productline_suffix = self.get_value(elem, "produclineSuffix")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, sid, productline_suffix,
                   transaction_id, validity_start_date, validity_end_date)
            ret.append(obj)
        return ret

    def run_query_measure_type(self, root):
        ret = []
        self.query = ".//Measure/measureType/[measureTypeId = '{item}']/..".format(
            item=self.query_id)
        for elem in root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            measure_sid = self.get_value(elem, "sid")
            goods_nomenclature_sid = self.get_value(elem, "goodsNomenclature/sid")
            goods_nomenclature_item_id = self.get_value(
                elem, "goodsNomenclature/goodsNomenclatureItemId")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            measure_type_id = self.get_value(elem, "measureType/measureTypeId")
            geographical_area_id = self.get_value(
                elem, "geographicalArea/geographicalAreaId")

            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, measure_sid, goods_nomenclature_item_id,
                   validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def run_query_geographical_area(self, root):
        ret = []
        self.query = ".//Measure/geographicalArea[geographicalAreaId = '{item}']/..".format(
            item=self.query_id)
        for elem in root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            measure_sid = self.get_value(elem, "sid")
            goods_nomenclature_sid = self.get_value(elem, "goodsNomenclature/sid")
            goods_nomenclature_item_id = self.get_value(
                elem, "goodsNomenclature/goodsNomenclatureItemId")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            measure_type_id = self.get_value(elem, "measureType/measureTypeId")
            geographical_area_id = self.get_value(
                elem, "geographicalArea/geographicalAreaId")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, measure_sid, goods_nomenclature_item_id,
                   validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def run_query_commodity_measure(self, root):
        ret = []
        self.query = ".//Measure/goodsNomenclature[goodsNomenclatureItemId = '{item}']/..".format(
            item=self.query_id)
        for elem in root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            measure_sid = self.get_value(elem, "sid")
            goods_nomenclature_sid = self.get_value(elem, "goodsNomenclature/sid")
            goods_nomenclature_item_id = self.get_value(
                elem, "goodsNomenclature/goodsNomenclatureItemId")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            measure_type_id = self.get_value(elem, "measureType/measureTypeId")
            geographical_area_id = self.get_value(
                elem, "geographicalArea/geographicalAreaId")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, measure_sid, goods_nomenclature_item_id,
                   validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def run_query_quota(self, root):
        ret = []
        self.query = ".//QuotaOrderNumber[quotaOrderNumberId = '{item}']/..".format(item=self.query_id)
        for elem in root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            quota_order_number_sid = self.get_value(elem, "sid")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, quota_order_number_sid,
                   validity_start_date, validity_end_date)
            ret.append(obj)
        return ret

    def get_value(self, elem, query):
        obj = elem.find(query, self.namespaces)
        if obj is None:
            return ""
        else:
            return obj.text
