#!/usr/bin/env python3

import argparse
import json
import time

def main():
    parser = argparse.ArgumentParser(description='Build Status Check Skill')
    parser.add_argument('task_id', nargs='?', help='Build task identifier')
    parser.add_argument('--ci', choices=['github', 'gitlab', 'jenkins'],
                       default='github', help='CI system')
    parser.add_argument('--branch', help='Branch name')
    parser.add_argument('--limit', type=int, default=3,
                       help='Limit build history')
    parser.add_argument('--watch', action='store_true',
                       help='Watch build status')
    parser.add_argument('--format', choices=['json', 'text', 'short'],
                       default='text', help='Output format')

    args = parser.parse_args()

    # Mock build data
    build_data = {
        'project': 'MyOS',
        'branch': args.branch or 'main',
        'taskId': args.task_id or '12345',
        'currentBuild': {
            'status': 'success',
            'triggeredBy': 'john.doe',
            'started': '2026-02-04T10:15:30Z',
            'duration': 923,
            'commit': {
                'hash': 'a1b2c3d4e5f6',
                'message': 'Add network stack improvements'
            }
        },
        'history': [
            {
                'id': '12345',
                'status': 'success',
                'duration': 923,
                'date': '2026-02-04T10:30:53Z'
            },
            {
                'id': '12344',
                'status': 'failed',
                'duration': 765,
                'date': '2026-02-04T09:45:22Z'
            },
            {
                'id': '12343',
                'status': 'success',
                'duration': 972,
                'date': '2026-02-03T14:22:10Z'
            }
        ]
    }

    # Limit history items
    build_data['history'] = build_data['history'][:args.limit]

    # Output in requested format
    if args.format == 'json':
        print(json.dumps(build_data, indent=2))
    elif args.format == 'short':
        print(f"{build_data['project']}#{build_data['taskId']}: {build_data['currentBuild']['status']}")
    else:  # text format
        print(f"""
Build Status Report
===================

Project: {build_data['project']}
Branch: {build_data['branch']}
Task ID: {build_data['taskId']}

Current Build:
- Status: Success
- Triggered by: {build_data['currentBuild']['triggeredBy']}
- Started: 2026-02-04 10:15:30 UTC
- Duration: 15m 23s
- Commit: {build_data['currentBuild']['commit']['hash']} "{build_data['currentBuild']['commit']['message']}"

Recent Builds:""")

        for i, build in enumerate(build_data['history'], 1):
            status_symbol = "✓" if build['status'] == 'success' else "✗"
            duration_min = build['duration'] // 60
            duration_sec = build['duration'] % 60
            print(f"{i}. #{build['id']} {status_symbol} {build['status'].title()} ({duration_min}m {duration_sec}s) - {build['date'][:10]}")

    # Watch mode simulation
    if args.watch:
        print("\nWatching build status... (Press Ctrl+C to stop)")
        try:
            while True:
                # In a real implementation, this would fetch updated status
                # Here we just simulate with a simple message
                time.sleep(5)
                print(f"[{time.strftime('%H:%M:%S')}] Build status unchanged: success")
        except KeyboardInterrupt:
            print("\nStopped watching build status.")

if __name__ == '__main__':
    main()