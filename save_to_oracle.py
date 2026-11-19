import oracledb

from oracle_db import get_connection


MERGE_SQL = """
MERGE INTO OCTANE_FEATURES tgt
USING (
    SELECT
        :id AS id
    FROM dual
) src
ON (tgt.id = src.id)

WHEN MATCHED THEN 
UPDATE SET
    tgt.business_analyst_udf = :business_analyst_udf,
    tgt.has_attachments = :has_attachments,
    tgt.name = :name,
    tgt.phase = :phase,
    tgt.plan_start_date_udf = :plan_start_date_udf,
    tgt.plan_end_date_udf = :plan_end_date_udf,
    tgt.data_classification = :data_classification,
    tgt.account_bucket_udf = :account_bucket_udf,
    tgt.tr05_document_type_udf = :tr05_document_type_udf,
    tgt.feature_size_udf = :feature_size_udf,
    tgt.brd_in_file_share = :brd_in_file_share,
    tgt.description = :description,
    tgt.uat_first_time_right_udf = :uat_first_time_right_udf,
    tgt.author = :author,
    tgt.owner = :owner,
    tgt.data_owner_udf = :data_owner_udf,
    tgt.developer_name_udf = :developer_name_udf,
    tgt.it_contact_udf = :it_contact_udf,
    tgt.priority = :priority,
    tgt.change_request_type_udf = :change_request_type_udf,
    tgt.application_modules = :application_modules,
    tgt.arbapprodate_udf = :arbapprodate_udf,
    tgt.enddate_udf = :enddate_udf,
    tgt.creation_time = :creation_time,
    tgt.last_modified = :last_modified,
    tgt.biz_app_coordinator_udf = :biz_app_coordinator_udf,
    tgt.business_case_udf = :business_case_udf,
    tgt.manday_udf = :manday_udf,
    tgt.techapprovaldate_udf = :techapprovaldate_udf,
    tgt.tech_filepath_udf = :tech_filepath_udf,
    tgt.tech_remark_udf = :tech_remark_udf,
    tgt.covering_tests = :covering_tests,
    tgt.test_data = :test_data,
    tgt.release_data = :release_data,
    tgt.intdeploycheck_udf = :intdeploycheck_udf,
    tgt.deploy_path_udf = :deploy_path_udf,
    tgt.release_remarks_udf = :release_remarks_udf,
    tgt.uat_res_person_udf = :uat_res_person_udf,
    tgt.teamwork_evaluation_udf = :teamwork_evaluation_udf,
    tgt.quality_of_deliverables_udf = :quality_of_deliverables_udf,
    tgt.deliverables_timeline_udf = :deliverables_timeline_udf,
    tgt.bizcasevalue_udf = :bizcasevalue_udf
    

WHEN NOT MATCHED THEN
INSERT (
    id,
    business_analyst_udf,
    has_attachments,
    name,
    phase,
    plan_start_date_udf,
    plan_end_date_udf,
    data_classification,
    account_bucket_udf,
    tr05_document_type_udf,
    feature_size_udf,
    brd_in_file_share,
    description,
    uat_first_time_right_udf,
    author,
    owner,
    data_owner_udf,
    developer_name_udf,
    it_contact_udf,
    priority,
    change_request_type_udf,
    application_modules,
    arbapprodate_udf,
    enddate_udf,
    creation_time,
    last_modified,
    biz_app_coordinator_udf,
    business_case_udf,
    manday_udf,
    techapprovaldate_udf,
    tech_filepath_udf,
    tech_remark_udf,
    covering_tests,
    test_data,
    release_data,
    intdeploycheck_udf,
    deploy_path_udf,
    release_remarks_udf,
    uat_res_person_udf,
    teamwork_evaluation_udf,
    quality_of_deliverables_udf,
    deliverables_timeline_udf,
    bizcasevalue_udf
)

VALUES (
    :id,
    :business_analyst_udf,
    :has_attachments,
    :name,
    :phase,
    :plan_start_date_udf,
    :plan_end_date_udf,
    :data_classification,
    :account_bucket_udf,
    :tr05_document_type_udf,
    :feature_size_udf,
    :brd_in_file_share,
    :description,
    :uat_first_time_right_udf,
    :author,
    :owner,
    :data_owner_udf,
    :developer_name_udf,
    :it_contact_udf,
    :priority,
    :change_request_type_udf,
    :application_modules,
    :arbapprodate_udf,
    :enddate_udf,
    :creation_time,
    :last_modified,
    :biz_app_coordinator_udf,
    :business_case_udf,
    :manday_udf,
    :techapprovaldate_udf,
    :tech_filepath_udf,
    :tech_remark_udf,
    :covering_tests,
    :test_data,
    :release_data,
    :intdeploycheck_udf,
    :deploy_path_udf,
    :release_remarks_udf,
    :uat_res_person_udf,
    :teamwork_evaluation_udf,
    :quality_of_deliverables_udf,
    :deliverables_timeline_udf,
    :bizcasevalue_udf
)
"""

def save_features(records):

    if not records:
        print("No records to save.")
        return
    
    conn = get_connection()

    if conn is None:
        print("Unable to connect to Oracle")
        return 

    cursor = conn.cursor()

    try:

        for record in records:
            for key, value in record.items():
                if isinstance(value, (dict, list)):
                    print(f"Dict/List found -> ID: {record['id']}")
                    print(f"Field: {key}")
                    print(value)
                    return

        cursor.executemany(
            MERGE_SQL,
            records
        )

        conn.commit()

        print("=" * 60)
        print(f"Successfully saved {len(records)} records into Oracle.")
        print("=" * 60)
    
    except Exception as e:

        conn.rollback()

        print("=" * 60)
        print("Database Error")
        print(e)
        print("=" * 60)

        print("\nChecking records\n")

        for record in records:
            try:

             cursor.execute(
                MERGE_SQL,
                record
             )
            
            except Exception as ex:

             print("-" * 60)
             print("Failed Record ID:", record.get("id"))
             print("Feature Name :", record.get("name"))
             print("Error :", ex)
             print("-" * 60)

             break

    finally:

        cursor.close()
        conn.close()

        print("Oracle Connection Closed")