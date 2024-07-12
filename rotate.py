import boto3
from datetime import timedelta, datetime, UTC


MAX_ACTIVE_TIME=timedelta(days=60)


def main():
    print("loading data...")
    try:
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
        active_keys = [k for k in user_keys if k["Status"] == "Active" and k["CreateDate"] + MAX_ACTIVE_TIME >= datetime.now(tz=UTC)]
        active_keys = sorted(active_keys, key=lambda k: k["CreateDate"], reverse=True)
        obsolete_keys = [k for k in user_keys if k["Status"] == "Active" and k["CreateDate"] + MAX_ACTIVE_TIME < datetime.now(tz=UTC)]
        obsolete_keys = sorted(obsolete_keys, key=lambda k: k["CreateDate"], reverse=True)
        inactive_keys = [k for k in user_keys if k["Status"] != "Active"]
        inactive_keys = sorted(inactive_keys, key=lambda k: k["CreateDate"], reverse=True)
        if len(obsolete_keys) == 0 and len(inactive_keys) == 0:
            print("no Obsolete and no Inactive keys: no action")
            return
        if len(inactive_keys) > 0:
            print(f"Removing Inactive key")
            oldest_inactive_key = inactive_keys[-1]
            client.delete_access_key(AccessKeyId=oldest_inactive_key["AccessKeyId"])
        if len(active_keys) == 0:
            if len(obsolete_keys) > 1:
                print(f"Multiple Obsolete keys, removing oldest")
                oldest_obsolete_key = obsolete_keys[-1]
                client.delete_access_key(AccessKeyId=oldest_obsolete_key["AccessKeyId"])
            print(f"No Active keys, creating...")
            new_key = client.create_access_key()
            print(f"REMEMBER TO SAVE THE KEY, AccessKeyId: {new_key['AccessKey']['AccessKeyId']}, SecretAccessKey: {new_key['AccessKey']['SecretAccessKey']}")
            return
        if len(active_keys) == 1:
            if len(obsolete_keys) > 0:
                print(f"Deactivating Obsolete key")
                oldest_obsolete_key = obsolete_keys[-1]
                client.update_access_key(AccessKeyId=oldest_obsolete_key["AccessKeyId"], Status='Inactive')
    finally:
        print("done")


if __name__ == "__main__":
    main()
