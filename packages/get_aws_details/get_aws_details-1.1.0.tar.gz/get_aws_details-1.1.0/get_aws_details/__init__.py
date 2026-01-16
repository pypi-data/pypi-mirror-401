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

import csv
import traceback
import itertools
import argparse
import boto3
import aws_crawler
from multithreader import threads
from aws_authenticator import AWSAuthenticator


__version__ = '1.1.0'
__author__ = 'Ahmad Ferdaus Abd Razak'
__application__ = 'aws_details'


def get_enabled_regions(client) -> list:
    """Get all enabled regions for an AWS account."""
    try:
        response = client.describe_regions(AllRegions=True)
        enabled_regions = [
            region.get('RegionName')
            for region in response['Regions']
            if region.get('OptInStatus') in ['opted-in', 'opt-in-not-required']
        ]

    except Exception as e:
        print(f'Error getting regions: {str(e)}')
        enabled_regions = []

    return enabled_regions


def main_action(account_id: str, items: dict) -> dict:
    """Execute main action in an AWS account."""
    print(f'Working on {account_id}...')

    if account_id != items['sso_account_id']:
        try:
            if items.get('assumed_role_name') is not None:
                credentials = aws_crawler.get_credentials(
                    items.get('session'),
                    f'arn:aws:iam::{account_id}:role/{items.get("assumed_role_name")}',
                    items.get('external_id')
                )
                ec2 = boto3.client(
                    'ec2',
                    aws_access_key_id=credentials.get('aws_access_key_id'),
                    aws_secret_access_key=credentials.get('aws_secret_access_key'),
                    aws_session_token=credentials.get('aws_session_token')
                )
            else:
                auth = AWSAuthenticator(
                    sso_url=items.get('sso_url'),
                    sso_role_name=items.get('sso_role_name'),
                    sso_account_id=account_id
                )
                session = auth.sso()
                ec2 = session.client('ec2')
            enabled_regions = get_enabled_regions(ec2)

            details = []
            for region in enabled_regions:
                if items.get('assumed_role_name') is not None:
                    client = boto3.client(
                        items.get('service'),
                        aws_access_key_id=credentials.get('aws_access_key_id'),
                        aws_secret_access_key=credentials.get('aws_secret_access_key'),
                        aws_session_token=credentials.get('aws_session_token'),
                        region_name=region
                    )
                else:
                    client = session.client(items.get('service'), region_name=region)
                paginator = client.get_paginator(items.get('command'))

                if len(items.get('Filters')) > 0:
                    response_iterator = paginator.paginate(Filters=items.get('Filters'))
                else:
                    response_iterator = paginator.paginate()

                for page in response_iterator:
                    contents = page[items.get('page_key')]
                    if len(contents) > 0:
                        for content in contents:
                            kvps_content = {
                                kvp.split('=')[0].replace(' ', ''): content.get(
                                    kvp.split('=')[1].replace(' ', '')
                                )
                                for kvp in items.get('kvps')
                            }
                            kvps_content['account_id'] = account_id
                            kvps_content['region'] = region
                            details.append(kvps_content)

        except Exception as e:
            tb_list = traceback.extract_tb(e.__traceback__)
            last_frame = tb_list[-1]
            line_number = last_frame.lineno
            details = [
                {
                    'account_id': account_id,
                    'exception': str(e),
                    'line_number': line_number
                }
            ]

    else:
        details = [
            {
                'account_id': account_id,
                'exception': 'Skipped master account.'
            }
        ]

    return details


def json_to_csv(data: list, output_file: str) -> None:
    """Convert JSON data to CSV and write to file."""
    clean_data = []
    if len(data) > 0:
        for item in data:
            if 'exception' not in item.keys():
                clean_data.append(item)
        if len(clean_data) > 0:
            with open(output_file, 'w', newline='') as output_file:
                keys = clean_data[0].keys()
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(clean_data)
        else:
            print('No clean data found.')
    else:
        print('No data found.')


def count_lines(output_file: str) -> int:
    """Count number of lines in a file."""
    with open(output_file, 'r') as f:
        lines = sum(1 for line in f)
    return lines


def get_params():
    """Get parameters from script inputs."""
    myparser = argparse.ArgumentParser(
        add_help=True,
        allow_abbrev=False,
        description=(
            'Get multi-region details from AWS Organizations accounts. '
            'View docstring for command line example.'
        ),
        usage=f'{__application__} [options]'
    )
    myparser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'{__application__} {__version__}'
    )
    myparser.add_argument(
        '-a',
        '--sso_account_id',
        action='store',
        help='SSO Account ID.',
        required=True,
        type=str
    )
    myparser.add_argument(
        '-u',
        '--sso_url',
        action='store',
        help='SSO URL.',
        required=True,
        type=str
    )
    myparser.add_argument(
        '-r',
        '--sso_role_name',
        action='store',
        help='SSO Role Name.',
        required=True,
        type=str
    )
    myparser.add_argument(
        '-n',
        '--assumed_role_name',
        action='store',
        help='Assumed Role Name (default: None).',
        nargs='?',
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        '-e',
        '--external_id',
        action='store',
        help='External ID for assumed role (default: None).',
        nargs='?',
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        '-s',
        '--account_statuses',
        action='store',
        help='Comma-separated account statuses to filter (default: None).',
        nargs='?',
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        '-o',
        '--account_ou',
        action='store',
        help='Account Organizational Unit to filter (default: None).',
        nargs='?',
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        '-l',
        '--account_list',
        action='store',
        help='Comma-separated list of account IDs to filter (default: None).',
        nargs='?',
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        '-t',
        '--thread_num',
        action='store',
        help='Number of threads to use for multithreading (default: 10).',
        nargs='?',
        default=10,
        required=False,
        type=int
    )
    myparser.add_argument(
        '-f',
        '--output_file',
        action='store',
        help='Path to the output CSV file (default: aws_details.csv).',
        nargs='?',
        default='aws_details.csv',
        required=False,
        type=str
    )
    myparser.add_argument(
        '-v',
        '--service',
        action='store',
        help='AWS service to query (example: ec2).',
        required=True,
        type=str
    )
    myparser.add_argument(
        '-p',
        '--page_key',
        action='store',
        help='Pagination key for the AWS service response (example: Vpcs).',
        required=True,
        type=str
    )
    myparser.add_argument(
        '-c',
        '--command',
        action='store',
        help='AWS service command to execute (example: describe_vpcs).',
        required=True,
        type=str
    )
    myparser.add_argument(
        '-k',
        '--kvps',
        action='store',
        help='Key-value pairs for CSV output (format: key=value).',
        nargs='+',
        required=True,
        type=str
    )
    myparser.add_argument(
        '-i',
        '--filters',
        action='store',
        help='Filters for AWS service query (format: Name=Values).',
        nargs='*',
        default=None,
        required=False,
        type=str
    )
    return myparser.parse_args()


def main():
    """Execute main function."""
    # Get parameters.
    args = get_params()
    sso_account_id = args.sso_account_id.replace(' ', '')
    sso_url = args.sso_url.replace(' ', '')
    sso_role_name = args.sso_role_name.replace(' ', '')
    account_statuses = args.account_statuses
    account_ou = args.account_ou
    account_list = args.account_list
    thread_num = args.thread_num
    output_file = args.output_file.replace(' ', '')
    service = args.service.replace(' ', '')
    page_key = args.page_key.replace(' ', '')
    command = args.command.replace(' ', '')
    kvps = args.kvps
    filters = args.filters
    assumed_role_name = (
        args.assumed_role_name.replace(' ', '')
        if args.assumed_role_name is not None else None
    )
    external_id = (
        args.external_id.replace(' ', '')
        if args.external_id is not None else None
    )

    # Prepare Filters for AWS service query.
    Filters = [
        {
            'Name': filter.split('=')[0].replace(' ', ''),
            'Values': filter.split('=')[1].replace(' ', '').split(',')
        } for filter in filters
    ] if filters is not None else []

    # Prepare items dictionary for multithreading.
    items = {
        'sso_url': sso_url,
        'sso_role_name': sso_role_name,
        'sso_account_id': sso_account_id,
        'assumed_role_name': assumed_role_name,
        'external_id': external_id,
        'service': service,
        'page_key': page_key,
        'command': command,
        'kvps': kvps,
        'Filters': Filters
    }

    # Login to AWS using SSO and create session.
    if assumed_role_name is not None:
        auth = AWSAuthenticator(
            sso_url=sso_url,
            sso_role_name=sso_role_name,
            sso_account_id=sso_account_id
        )
        session = auth.sso()
        items['session'] = session

    # Get list of account IDs based on parameters.
    if account_statuses is not None:
        account_ids = aws_crawler.list_accounts(session, account_statuses.replace(' ', ''))
    elif account_ou is not None:
        account_ids = aws_crawler.list_ou_accounts(session, account_ou.replace(' ', ''))
    elif account_list is not None and assumed_role_name is not None:
        account_ids = aws_crawler.create_account_list(account_list.replace(' ', ''))
    elif account_list is not None and assumed_role_name is None:
        account_ids = aws_crawler.create_account_list(account_list.replace(' ', ''))
    else:
        pass

    # Execute main action.
    if account_list is not None and assumed_role_name is None:
        res = [main_action(account_id, items) for account_id in account_ids]
    else:
        res = threads(main_action, account_ids, items, thread_num=thread_num)

    # Combine results and write to CSV.
    results = list(itertools.chain.from_iterable(res))
    json_to_csv(results, output_file)
    print(f'Found {count_lines(output_file) - 1} records.')
