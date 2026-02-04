#!/usr/bin/env python3

import argparse
import json
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='Version Query Skill')
    parser.add_argument('--source', choices=['config', 'git', 'build', 'auto'],
                       default='auto', help='Version source')
    parser.add_argument('--format', choices=['json', 'text', 'short'],
                       default='text', help='Output format')
    parser.add_argument('--include-metadata', action='store_true',
                       help='Include metadata')

    args = parser.parse_args()

    # Mock version data
    output_data = {
        'project': 'MyOS',
        'version': 'v2.1.3',
        'source': args.source if args.source != 'auto' else 'git'
    }

    # Add metadata if requested
    if args.include_metadata:
        output_data['commit'] = 'a1b2c3d4e5f6'
        output_data['buildDate'] = '2026-02-04T10:30:00Z'

    # Output in requested format
    if args.format == 'json':
        print(json.dumps(output_data, indent=2))
    elif args.format == 'short':
        print(output_data['version'])
    else:
        print(f"Project: {output_data['project']}")
        print(f"Version: {output_data['version']}")
        print(f"Source: {output_data['source']}")
        if args.include_metadata:
            print(f"Commit: {output_data['commit']}")
            print(f"Build Date: {output_data['buildDate']}")


if __name__ == '__main__':
    main()