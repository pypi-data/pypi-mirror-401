
import argparse, sys, os
from .infer import detect_schema, write_schema
from .exceptions import ArgumentError

# NOTE: Preserves all existing arguments. Adds no removals.
def build_parser():
    p = argparse.ArgumentParser(
        prog='schema-detect',
        description='Detect and infer schema from files/directories.'
    )
    p.add_argument('path', nargs='?', help='Input file or directory path')
    p.add_argument('--config', help='Path to YAML config to override flags')
    p.add_argument('--detection-mode', choices=['trust_hint','verify_hint','auto_detect'], default='trust_hint')
    p.add_argument('--coverage-mode', choices=['any','max','full'], default='max')
    p.add_argument('--sample-records', type=int, default=500)
    p.add_argument('--sample-bytes', default='5MB')
    p.add_argument('--output-dir', help='Directory to write output files')
    p.add_argument('--output-file', default='schema.yml', help='Output file name')
    p.add_argument('--fmt', choices=['yaml','json','txt','dict'], default='yaml')
    p.add_argument('--zip-max-size', default='500MB')
    p.add_argument('--zip-max-members', type=int, default=100)
    p.add_argument('--sample-total-bytes-cap', default='1GB')
    p.add_argument('--max-file-size', default='50GB')
    p.add_argument('--max-workers', type=int, default=None)
    p.add_argument('--retries', type=int, default=3)
    p.add_argument('--timeout-seconds', type=int, default=180)
    p.add_argument('--log-json', action='store_true')
    p.add_argument('-v','--verbose', action='count', default=0)
    p.add_argument('--multi-file-fmt', default='schema.yml', help='File extension for multi-file schema outputs')

    # CSV overrides
    p.add_argument('--csv.header', choices=['auto','true','false'], default='auto')
    p.add_argument('--csv.delimiter')
    p.add_argument('--csv.quote')
    p.add_argument('--csv.escape')
    p.add_argument('--encoding', choices=['utf-8','utf-8-sig','utf-16le','utf-16be'])
    return p


def main(argv=None):
    argv = argv or sys.argv[1:]
    args = build_parser().parse_args(argv)
    if not args.path:
        raise ArgumentError('Path is required')
    if not os.path.exists(args.path):
        raise ArgumentError(f'Input path does not exist: {args.path}')

    # Pass through all relevant flags to detect_schema
    schema = detect_schema(
        input_path=args.path,
        detection_mode=args.detection_mode,
        coverage_mode=args.coverage_mode,
        sample_records=args.sample_records,
        csv_header=getattr(args,'csv.header'),
        csv_delimiter=getattr(args,'csv.delimiter'),
        encoding=args.encoding,
        sample_bytes=args.sample_bytes,
        zip_max_size=args.zip_max_size,
        zip_max_members=args.zip_max_members,
        sample_total_bytes_cap=args.sample_total_bytes_cap,
        max_file_size=args.max_file_size,
        retries=args.retries,
        timeout_seconds=args.timeout_seconds,
        log_json=args.log_json,
        verbosity=args.verbose,
        max_workers=args.max_workers,
    )

    if args.fmt == 'dict':
        # Print the raw dict for programmatic consumption
        print(schema)
    else:
        write_schema(
            schema,
            out_dir=args.output_dir or '.',
            fmt=args.fmt,
            output_file=args.output_file,
            multi_file_fmt=args.multi_file_fmt,
        )


if __name__ == '__main__':
    main()
