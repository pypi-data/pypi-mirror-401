import argparse, sys, json, os
from .verify import verify_schema, write_report

def build_parser():
    p = argparse.ArgumentParser(
        prog='schema-verify',
        description='Verify two schema outputs (files/DFs) for fields/types/nullability/patterns.'
    )
    p.add_argument('left', help='Left schema path or data path')
    p.add_argument('right', help='Right schema path or data path')
    p.add_argument('--case-insensitive', action='store_true')
    p.add_argument('--order-sensitive', action='store_true')
    p.add_argument('--relaxed-types', action='store_true')
    p.add_argument('--nullable-strict', action='store_true')
    p.add_argument('--pattern-mode', choices=['exact','glob','regex'])
    p.add_argument('--dir-mode', choices=['first','any','all'], default='first')
    p.add_argument('--fmt', choices=['yaml','json','txt','dict'], default='txt')
    p.add_argument('--output', help='Full path to output report file')
    p.add_argument('--output-dir', default='.', help='Directory for output report')
    p.add_argument('--output-file', help='File name for output report')
    return p


def main(argv=None):
    argv = argv or sys.argv[1:]
    args = build_parser().parse_args(argv)


    missing = []
    if isinstance(args.left, str) and not os.path.exists(args.left):
        missing.append(("left", args.left))
    if isinstance(args.right, str) and not os.path.exists(args.right):
        missing.append(("right", args.right))

    if missing:
        report = {
            "ok": False,
            "summary": "missing input file(s)",
            "details": {
                "missing": [{"side": side, "path": path} for side, path in missing]
            }
        }

        # Print to stdout in the requested format and exit non-zero
        if args.fmt in ('json', 'dict'):
            print(json.dumps(report, indent=2))
        elif args.fmt == 'yaml':
            try:
                import yaml
                print(yaml.safe_dump(report, sort_keys=False))
            except Exception:
                print(json.dumps(report, indent=2))
        else:
            lines = []
            lines.append("Result: MISSING INPUT(S)")
            for side, path in missing:
                lines.append(f"Missing {side} path: {path}")
            print('\n'.join(lines))
        sys.exit(2)

    report = verify_schema(
        left=args.left,
        right=args.right,
        case_sensitive=not args.case_insensitive,
        order_sensitive=args.order_sensitive,
        relaxed_types=args.relaxed_types,
        nullable_strict=args.nullable_strict,
        pattern_mode=args.pattern_mode,
        dir_mode=args.dir_mode,
    )

    ok = report.get('ok', False)

    if args.output:
        write_report(report, fmt=args.fmt, output_path=args.output, output_dir=args.output_dir)
    elif args.output_file:
        write_report(report, fmt=args.fmt, output_dir=args.output_dir, output_file=args.output_file)
    else:
        # Print to stdout (legacy behavior)
        if args.fmt in ('json','dict'):
            print(json.dumps(report, indent=2))
        elif args.fmt == 'yaml':
            try:
                import yaml
                print(yaml.safe_dump(report, sort_keys=False))
            except Exception:
                print(json.dumps(report, indent=2))
        else:
            # TXT summary
            details = report.get('details', {})
            lines = []
            lines.append(f"Result: {'OK' if ok else 'MISMATCH'}")
            fs = details.get('field_summary')
            if fs:
                matched = fs.get('matched_fields', [])
                left_only = fs.get('left_only_fields', [])
                right_only = fs.get('right_only_fields', [])
                lines.append('Common fields (order as in left): ' + (', '.join(matched) if matched else '(none)'))
                lines.append('Left-only:   ' + (', '.join(left_only) if left_only else '(none)'))
                lines.append('Right-only:  ' + (', '.join(right_only) if right_only else '(none)'))
            if details.get('mismatches'):
                lines.append('Mismatches:')
                for m in details['mismatches']:
                    lines.append(f"  - {m}")
            if details.get('warnings'):
                lines.append('Warnings:')
                for w in details['warnings']:
                    lines.append(f"  - {w}")
            print('\n'.join(lines))

    # Restore exit codes: 0=success, 1=mismatch
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
