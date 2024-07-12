# Check and rotate AWS access keys

After running this tool there should be at least one active key that was created in the last 60 days.

Keys older than 60 days are considered *Obsolete*.

AWS has a limit of two keys per user.

| Active | Obsolete | Inactive | All  | Comment                     |
|--------|----------|----------|------|-----------------------------|
| 0      | 0        | 0        | 0    | no active keys              |
| 0      | 0        | 1        | 1    | no active keys              |
| 0      | 0        | 2        | 2    | no active keys              |
| 0->1   | 1        | 0        | 1->2 | add active                  |
| 0->1   | 1        | 1->0     | 2    | remove inactive, add active |
| 0->1   | 2->1     | 0        | 2    | remove obsolete, add active |
| 1      | 0        | 0        | 1    | no action                   |
| 1      | 0        | 1->0     | 2->1 | remove inactive             |
| 1      | 1->0     | 0->1     | 2    | deactivate obsolete         |
| 2      | 0        | 0        | 2    | no action                   |

The following policy must be in place to run this tool:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "iam:DeleteAccessKey",
                "iam:UpdateAccessKey",
                "iam:CreateAccessKey",
                "iam:ListAccessKeys"
            ],
            "Resource": "arn:aws:iam::<account id>:user/${aws:username}"
        }
    ]
}
```

Replace `<account id>` and make sure that matching with `${aws:username}` is in place.