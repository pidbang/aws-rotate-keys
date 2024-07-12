import boto3
from datetime import timedelta, datetime, UTC


MAX_ACTIVE_TIME=timedelta(days=60)


def main():
    print("loading data...")
    client = boto3.client('iam')
    pagination_config = {
            'MaxItems': 1000,
            'PageSize': 10,
        }
    user_keys = []
    paginator = client.get_paginator('list_access_keys')
    keys_page_iterator = paginator.paginate(
        PaginationConfig=pagination_config
    )
    for keys_page in keys_page_iterator:
        for key in keys_page["AccessKeyMetadata"]:
            user_keys.append(key)
    active_keys = sum((1 for k in user_keys if k["Status"] == "Active" and k["CreateDate"] + MAX_ACTIVE_TIME >= datetime.now(tz=UTC)))
    obsolete_keys = sum((1 for k in user_keys if k["Status"] == "Active" and k["CreateDate"] + MAX_ACTIVE_TIME < datetime.now(tz=UTC)))
    inactive_keys = sum((1 for k in user_keys if k["Status"] != "Active"))
    print(f"active: {active_keys}, obsolete: {obsolete_keys}, inactive: {inactive_keys}, all: {len(user_keys)}")
    print("done")


if __name__ == "__main__":
    main()
