from datetime import datetime
from bs4 import BeautifulSoup
import json

def clean_html(text):

    if not text:
        return None
    
    return BeautifulSoup(
        text,
        "html.parser"
    ).get_text(" ", strip=True)

def parse_date(value):

    if not value:
        return None
    
    try:
        return datetime.strptime(
            value,
            "%Y-%m-%dT%H:%M:%SZ"
        )
    except:
        return None

def get_name(value):

    if value is None:
        return None

    if isinstance(value, dict):
        return value.get("name") or value.get("full_name")
    
    return value

def convert_json(value):

    if value is None:
        return None
    
    if isinstance(value, (dict,list)):

        return json.dumps(
            value,
            ensure_ascii=False
        )
    
    return value

def get_collection_full_name(value):

    if not value:
        return None
    
    data = value.get("data", [])

    if not data:
        return None
    
    return data[0].get("full_name")

def get_collection_name(value):

    if value is None:
        return None
    
    data = value.get("data", [])

    if not data:
        return None

    return data[0].get("name")

def get_collection_names(value):

    if not value:
        return None
    
    data = value.get("data", [])

    names = [
        person.get("name")
        for person in data
        if person.get("name")
    ]

    return ";".join(names) if names else None

def get_full_names(value):
    if not value:
        return None
    
    data = value.get("data", [])

    names = [
        person.get("full_name")
        for person in data
        if person.get("full_name")
    ]

    return "; ".join(names) if names else None

def get_names(value):
    if not value:
        return None
    
    data = value.get("data", [])

    names = [
        person.get("name")
        for person in data
        if person.get("name")
    ]

    return ";".join(names) if names else None


def parse_features(response_json):

    items = response_json.get("data", [])

    records = []

    for item in items:

        record = {

            "id":
                item.get("id"),
            "name":
                item.get("name"),
            "description":
                clean_html(item.get("description")),
            "data_classification":
                get_name(item.get("feature_type")),
            "author":
                get_name(item.get("author")),
            "owner":
                get_name(item.get("owner")),
            "priority":
                get_name(item.get("priority")),
            "phase":
                get_name(item.get("phase")),
            "uat_first_time_right_udf":
                get_name(item.get("uat_first_time_right_udf")),
            "teamwork_evaluation_udf":
                get_name(item.get("teamwork_evaluation_udf")),
            "quality_of_deliverables_udf":
                get_name(item.get("quality_of_deliverables_udf")),
            "deliverables_timeline_udf":
                get_name(item.get("deliverables_timeline_udf")),
            "release_remarks_udf":
                item.get("release_remarks_udf"),
            "techapprovaldate_udf":
                parse_date(item.get("techapprovaldate_udf")),
            "tech_filepath_udf":
                item.get("tech_filepath_udf"),
            "tech_remark_udf":
                item.get("tech_remark_udf"),
            "business_case_udf":
                item.get("business_case_udf"),
            "it_contact_udf":
                get_full_names(
                    item.get("it_contact_udf")
                ),
            "change_request_type_udf":
                get_names(
                    item.get("change_request_type_udf")
                ),
            "biz_app_coordinator_udf":
                get_collection_full_name(
                    item.get("biz_app_coordinator_udf")
                ),
            "feature_size_udf":
                get_name(item.get("feature_size_udf")),
            "tr05_document_type_udf":
                item.get("tr05_document_type_udf"),
            "developer_name_udf":
                get_name(
                    item.get("developer_name_udf")
                ),
            "business_analyst_udf":
                get_name(
                    item.get("business_analyst_udf")
                ),
            "data_owner_udf":
                get_name(item.get("data_owner_udf")),
            "plan_start_date_udf":
                parse_date(item.get("plan_start_date_udf")),
            "plan_end_date_udf":
                parse_date(item.get("plan_end_date_udf")),
            "release_data":
                get_name(item.get("release")),
            "covering_tests":
                convert_json(item.get("covering_tests")),
            "test_data":
                    get_names(item.get("test")),
            "creation_time":
                parse_date(item.get("creation_time")),
            "last_modified":
                parse_date(item.get("last_modified")),
            "has_attachments":
                1 if item.get("has_attachments") else 0,
            "account_bucket_udf":
                get_collection_name(
                    item.get("account_bucket_udf")
                ),
            "brd_in_file_share":
                get_name(item.get("brdchecklist_udf")),
            "application_modules":
                get_names(item.get("product_areas")),
            "arbapprodate_udf":
                parse_date(item.get("arbapprodate_udf")),
            "enddate_udf":
                parse_date(item.get("enddate_udf")),
            "manday_udf":
                convert_json(item.get("manday_udf")),
            "intdeploycheck_udf":
                get_name(item.get("intdeploycheck_udf")),
            "deploy_path_udf":
                item.get("deploy_path_udf"),
            "uat_res_person_udf":
                get_full_names(item.get("uat_res_person_udf")),
            "bizcasevalue_udf":
                convert_json(item.get("bizcasevalue_udf"))
        }

        records.append(record)

    return records