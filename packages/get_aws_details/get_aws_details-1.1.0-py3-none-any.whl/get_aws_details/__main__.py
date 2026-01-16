#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""
Get multi-region details from AWS Organizations accounts.

- SSO authentication
- Pagination (see caveat)
- Multithreading
- CSV output

Command line example:
$ aws_details \\
    -a 123456789012 \\
    -u https://my-sso-url.awsapps.com/start/#/ \\
    -r MySSORoleName \\
    -n MyAssumedRoleName \\
    -e MyExternalID \\
    -s ACTIVE \\
    -t 10 \\
    -f aws_details.csv \\
    -v ec2 \\
    -p Vpcs \\
    -c describe_vpcs \\
    -k vpc_id=VpcId cidr=CidrBlock is_default=IsDefault \\
    -i cidr=10.0.0.0/8

Caveat: Works with paginated AWS service commands only.
"""

import __init__

if __name__ == "__main__":
    __init__.main()
