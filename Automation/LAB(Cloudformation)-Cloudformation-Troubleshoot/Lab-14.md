# Lab 14 - CloudFormation Troubleshooting Journey

## 📘 Overview

I launched a CloudFormation stack, it failed during creation, I prevented automatic rollback so I could inspect resources, diagnosed the failing user-data / WaitCondition, fixed the template, recreated the stack successfully, added an object to the S3 bucket for drift testing, and finally deleted the stack while preserving the S3 bucket and its files.

---

## 🎯 Goal

- Stop automatic rollback on failure so failed resources remain for inspection.
- Find why the stack failed (user-data → WaitCondition).
- Fix the template and recreate the stack.
- Add an object to the S3 bucket and detect drift.
- Delete the stack while retaining the S3 bucket and its contents.

---

## 🧰 Tools Used

AWS CLI • CloudFormation • EC2 • S3 • JMESPath

---

## Architecture

![Architecture Diagram](screenshots/Architecture.png)

---

## 🛠️ Corrected Steps Performed

### Step 1 — First stack create (it fails)

1. Kick off the stack:

```bash
aws cloudformation create-stack \
  --stack-name myStack \
  --template-body file://template1.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters ParameterKey=KeyName,ParameterValue=vockey

```

1. Watch resources to see progress:

```bash
watch -n 5 -d aws cloudformation describe-stack-resources --stack-name myStack --query 'StackResources[*].[ResourceType,ResourceStatus]' --output table

```

![Stack Create Failed with Rollback](screenshots/StackCreateFailed.png)

Stack goes to **CREATE_FAILED** / **ROLLBACK_IN_PROGRESS** quickly.

📌 | At this point the resources are being deleted automatically because rollback is on by default.

---

### Step 2 — Prevent rollback (so I can inspect the failed instance)

**This is the step I messed up earlier.** Do **not** upload files yet. Instead, re-create the stack but prevent rollback so the resources persist for debugging.

Correct command (use the lab-recommended flag):

```bash
aws cloudformation create-stack \
  --stack-name myStack \
  --template-body file://template1.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --on-failure DO_NOTHING \
  --parameters ParameterKey=KeyName,ParameterValue=vockey

```

or equivalently:

```bash
aws cloudformation create-stack ... --disable-rollback

```

(the activity uses `--on-failure DO_NOTHING` in Task 2.4 — use that if you want exact lab parity).

Wait until stack finishes attempting creation (it will show **CREATE_FAILED** but *won’t* roll resources back).

📌 | Preventing rollback keeps the EC2 instance and other resources around so you can inspect logs and scripts. Do **not** upload any files to the S3 bucket yet — that comes after the stack is successfully created in a later step.

---

### Step 3 — Inspect stack events and find the failing resource

1. Show only the failing events:

```bash
aws cloudformation describe-stack-events --stack-name myStack --query "StackEvents[?ResourceStatus == 'CREATE_FAILED']"

```

1. You’ll likely see the WaitCondition as the failing resource:

```
"ResourceType": "AWS::CloudFormation::WaitCondition",
"ResourceStatusReason": "WaitCondition timed out. Received 0 conditions when expecting 1"

```

📌 | WaitCondition timed out = EC2 userdata didn't send cfn-signal.

---

### Step 4 — SSH into the Web Server instance and check userdata logs

1. Find the instance public IP (example query):

```bash
aws ec2 describe-instances --filters "Name=tag:Name,Values='Web Server'" --query 'Reservations[].Instances[].[State.Name,PublicIpAddress]' --output text

```

1. SSH to the instance (use your key), then check cloud-init output:

```bash
tail -50 /var/log/cloud-init-output.log

```

1. View the exact userdata script that ran:

```bash
sudo cat /var/lib/cloud/instance/scripts/part-001

```

Look for the script header and failing line:

```bash
#!/bin/bash -xe
# ...
yum install -y http    # <-- this fails because pkg name is wrong
# ... then the script never reaches cfn-signal

```

![Userdata Error in Cloud-Init Log](screenshots/UserdataErrorLog.png)

📌 | `-e` causes immediate exit on the failed yum command; no cfn-signal is sent → WaitCondition times out.

---

### Step 5 — Fix the template (edit userdata), then delete the failed stack

1. Edit `template1.yaml` on the CLI Host: change `http` → `httpd` in the yum install line.

```bash
vim template1.yaml   # or sed/awk if you prefer
# make changes, save
```

1. Confirm the change:

```bash
cat template1.yaml | grep httpd

```

1. Delete the **failed** stack (the one with CREATE_FAILED):

```bash
aws cloudformation delete-stack --stack-name myStack

```

1. Wait until it’s gone:

```bash
aws cloudformation wait stack-delete-complete --stack-name myStack
# or poll describe-stacks until it no longer exists

```

📌 | Deleting the failed stack clears previous attempted resources so you can re-create cleanly with the fix.

---

### Step 6 — Recreate the stack with the fix (no rollback required now)

Run the create-stack again (fixed template). You can choose to keep `--on-failure DO_NOTHING` while confirming success, but generally:

```bash
aws cloudformation create-stack \
  --stack-name myStack \
  --template-body file://template1.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --on-failure DO_NOTHING \
  --parameters ParameterKey=KeyName,ParameterValue=vockey

```

Watch resources:

```bash
watch -n 5 -d aws cloudformation describe-stack-resources --stack-name myStack --query 'StackResources[*].[LogicalResourceId,ResourceType,ResourceStatus]' --output table

```

![Stack Create Complete with Fixed Template](screenshots/StackCreateComplete.png)

Expectation: WaitCondition receives signal, stack reaches **CREATE_COMPLETE**.

📌 | Now your EC2 userdata runs successfully, calls `cfn-signal` and the WaitCondition passes.

---

### Step 7 — Task 3: Add an object to the S3 bucket (drift test)

Once stack is **CREATE_COMPLETE**, get the bucket name from outputs:

```bash
bucketName=$(aws cloudformation describe-stacks \
  --stack-name myStack \
  --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" \
  --output text)
echo "bucketName = $bucketName"

```

Create and upload a test file:

```bash
touch myfile
aws s3 cp myfile s3://$bucketName/
aws s3 ls s3://$bucketName/

```

📌 |Note:  Adding objects to a bucket does not count as drift; changing bucket properties would.

---

### Step 8 — Detect drift on the stack (showing the manual change)

1. Start drift detection:

```bash
driftId=$(aws cloudformation detect-stack-drift --stack-name myStack --query "StackDriftDetectionId" --output text)

```

1. Check detection status (poll until COMPLETE):

```bash
aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id $driftId --query "StackDriftStatus"

```

![Drift Detection Status](screenshots/DriftDetectionStatus.png)

1. Show resource-level drift:

```bash
aws cloudformation describe-stack-resources --stack-name myStack --query 'StackResources[*].[ResourceType,ResourceStatus,DriftInformation.StackResourceDriftStatus]' --output table

```

📌 | Note: The security group that is manually modified should show `MODIFIED` — the bucket will show `IN_SYNC` because adding objects isn't considered a property drift.

---

### Step 9 — Task 4: Attempt to delete the stack (this time it will fail because bucket is not empty)

Try deleting the stack:

```bash
aws cloudformation delete-stack --stack-name myStack

```

Watch resources deleting:

```bash
watch -n 5 -d aws cloudformation describe-stack-resources --stack-name myStack --query 'StackResources[*].[LogicalResourceId,ResourceType,ResourceStatus]' --output table

```

![Stack Delete Failed - Bucket Not Empty](screenshots/StackDeleteFailed.png)

Deletion will fail for the S3 bucket (DELETE_FAILED) because the bucket contains objects.

📌 | Note: CloudFormation refuses to delete a non-empty bucket to prevent data loss.

---

### Step 10 — Final Challenge: Delete the stack but retain the bucket and its file(s)

1. Get the bucket’s logical resource ID (JMESPath to the rescue):

```bash
aws cloudformation describe-stack-resources \
  --stack-name myStack \
  --query "StackResources[?ResourceType=='AWS::S3::Bucket'].LogicalResourceId" \
  --output text

```

Suppose it prints: `MyBucket`

1. Delete the stack while retaining that logical resource:

```bash
aws cloudformation delete-stack \
  --stack-name myStack \
  --retain-resources MyBucket

```

1. Wait for completion:

```bash
aws cloudformation wait stack-delete-complete --stack-name myStack

```

1. Confirm stack gone and bucket still there:

```bash
aws cloudformation describe-stacks --stack-name myStack --query "Stacks[0].StackStatus" --output text  # should error if stack gone
aws s3 ls s3://$bucketName/

```

📌 | The bucket and its objects remain intact in your account — they are simply no longer managed by CloudFormation.

---

## 📝 Key Takeaways

- Don’t upload or manipulate S3 objects until the stack is successfully created (I mistakenly suggested it earlier). The correct order: create → fix → recreate → *then* add files for drift testing.
- Use `-on-failure DO_NOTHING` (or `-disable-rollback`) to keep failed resources available for debugging. The lab uses `-on-failure DO_NOTHING`.
- Inspect stack events and cloud-init logs to find the root cause (user-data + `e` can abort early).
- Use `-retain-resources` with the LogicalResourceId to delete a stack while preserving specific resources like non-empty buckets.
- JMESPath `-query` is extremely helpful for extracting just the LogicalResourceId or Outputs.