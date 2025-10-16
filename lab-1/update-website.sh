#!/bin/bash
aws s3 cp ~/sysops-activity-files/static-website/ \
  s3://<bucket-name>/ --recursive --acl public-read