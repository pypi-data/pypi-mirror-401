"""Schema verification with cleaner single-file reporting and original-order field output.
- Keeps matched_pairs/unmatched_pairs ONLY for multi-file inputs.
- Preserves original order in field mismatch details.
- Adds field_summary (matched_fields, left_only_fields, right_only_fields) in details.
"""
from typing import Union, Dict, Any, List, Tuple
import os
import json
import pathlib

from .infer import detect_schema


def _load_schema(obj: Union[str, dict, Any]) -> Dict[str, Any]:
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, 'schema') or hasattr(obj, 'columns'):
        if hasattr(obj, 'schema'):
            return detect_schema(spark_df=obj)
        else:
            return detect_schema(pandas_df=obj)
    if isinstance(obj, str):
        path = os.path.normpath(obj)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Schema file does not exist: {path}")
        ext = os.path.splitext(path)[1].lower()
        if ext in ('.yml', '.yaml', '.json'):
            try:
                if ext in ('.yml', '.yaml'):
                    import yaml
                    with open(path, 'r', encoding='utf-8') as f:
                        doc = yaml.safe_load(f)
                        return doc if isinstance(doc, dict) else {"type": "struct", "fields": []}
                else:
                    with open(path, 'r', encoding='utf-8') as f:
                        doc = json.load(f)
                        return doc if isinstance(doc, dict) else {"type": "struct", "fields": []}
            except Exception:
                return {"type": "struct", "fields": []}
        return detect_schema(input_path=path)
    return {"type": "struct", "fields": []}


def _fields_list(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    fields = schema.get('fields')
    return list(fields) if isinstance(fields, list) else []


def _names_in_order(fields: List[Dict[str, Any]]) -> List[str]:
    return [str(f.get('name')) for f in fields]


def _compare_single(left: Dict[str, Any], right: Dict[str, Any], *,
                    compare: List[str],
                    case_sensitive: bool,
                    order_sensitive: bool,
                    relaxed_types: bool,
                    nullable_strict: bool,
                    pattern_mode: str = None) -> Tuple[bool, Dict[str, Any]]:
    mismatches: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    lf = _fields_list(left)
    rf = _fields_list(right)

    def norm_name(n: str) -> str:
        return n if case_sensitive else (n.lower() if isinstance(n, str) else n)

    left_names_order = _names_in_order(lf)
    right_names_order = _names_in_order(rf)

    # ---- Fields ----
    field_summary = None
    if 'fields' in compare:
        if order_sensitive or 'order' in compare:
            ln = [norm_name(n) for n in left_names_order]
            rn = [norm_name(n) for n in right_names_order]
            if ln != rn:
                mismatches.append({'kind': 'fields_order', 'left': left_names_order, 'right': right_names_order})
        else:
            ln_set = {norm_name(n) for n in left_names_order}
            rn_set = {norm_name(n) for n in right_names_order}
            if ln_set != rn_set:
                # Preserve original order in mismatch display
                mismatches.append({'kind': 'fields', 'left': left_names_order, 'right': right_names_order})
            # Build field_summary preserving original order
            matched = [n for n in left_names_order if norm_name(n) in rn_set]
            left_only = [n for n in left_names_order if norm_name(n) not in rn_set]
            right_only = [n for n in right_names_order if norm_name(n) not in ln_set]
            field_summary = {
                'matched_fields': matched,
                'left_only_fields': left_only,
                'right_only_fields': right_only,
            }

    # Align maps for downstream checks
    lmap = {norm_name(f.get('name')): f for f in lf}
    rmap = {norm_name(f.get('name')): f for f in rf}

    # ---- Types ----
    if 'types' in compare and not any(m['kind'].startswith('fields_order') for m in mismatches):
        def type_str(f: Dict[str, Any]) -> str:
            return str(f.get('type'))
        for name_key, lf_field in lmap.items():
            rt_field = rmap.get(name_key)
            lt = type_str(lf_field)
            rt = type_str(rt_field or {})
            if lt != rt:
                if relaxed_types:
                    if (lt == 'integer' and rt == 'double') or (lt == 'double' and rt == 'integer'):
                        continue
                    if (lt == 'decimal' and rt == 'double') or (lt == 'double' and rt == 'decimal'):
                        warnings.append({'kind': 'types_relaxed', 'field': lf_field.get('name'), 'left': lt, 'right': rt, 'message': 'decimal vs double: precision risk'})
                        continue
                    if (lt == 'date' and rt == 'timestamp') or (lt == 'timestamp' and rt == 'date'):
                        warnings.append({'kind': 'types_relaxed', 'field': lf_field.get('name'), 'left': lt, 'right': rt, 'message': 'date vs timestamp: potential loss of time portion'})
                        continue
                mismatches.append({'kind': 'types', 'field': lf_field.get('name'), 'left': lt, 'right': rt})

    # ---- Nullable ----
    if 'nullable' in compare:
        for name_key in set(lmap.keys()).intersection(rmap.keys()):
            ln = bool(lmap[name_key].get('nullable', False))
            rn = bool(rmap[name_key].get('nullable', False))
            if ln != rn:
                entry = {'kind': 'nullable', 'field': lmap[name_key].get('name'), 'left': ln, 'right': rn}
                if nullable_strict:
                    mismatches.append(entry)
                else:
                    warnings.append(entry)

    # ---- Patterns ---- (unchanged semantics, optional)
    if pattern_mode and ('patterns' in compare or 'pattern' in compare):
        def _meta(s: Dict[str, Any]) -> Dict[str, Any]:
            m = s.get('meta') or {}
            return {'pattern': m.get('file_name_pattern'), 'regex': m.get('file_name_regex'), 'file': m.get('file_name')}
        lm = _meta(left)
        rm = _meta(right)
        if pattern_mode == 'exact':
            if (lm.get('pattern') or '') != (rm.get('pattern') or ''):
                warnings.append({'kind': 'pattern_exact', 'left': lm, 'right': rm, 'message': 'patterns differ'})
        elif pattern_mode == 'glob':
            lp = (lm.get('pattern') or '')
            rp = (rm.get('pattern') or '')
            def _canon(p: str) -> str:
                return p.replace('*', '.*')
            if _canon(lp) != _canon(rp):
                warnings.append({'kind': 'pattern_glob', 'left': lm, 'right': rm, 'message': 'glob patterns differ'})
        elif pattern_mode == 'regex':
            lr = (lm.get('regex') or '')
            rr = (rm.get('regex') or '')
            if lr != rr:
                warnings.append({'kind': 'pattern_regex', 'left': lm, 'right': rm, 'message': 'regex patterns differ'})

    ok = len(mismatches) == 0
    detail = {'mismatches': mismatches, 'warnings': warnings}
    if field_summary is not None:
        detail['field_summary'] = field_summary
    return ok, detail


def verify_schema(left: Union[dict, str, Any], right: Union[dict, str, Any], *,
                  compare: List[str] = ['fields', 'types', 'nullable'],
                  case_sensitive: bool = True,
                  order_sensitive: bool = False,
                  relaxed_types: bool = False,
                  nullable_strict: bool = False,
                  pattern_mode: str = None,
                  dir_mode: str = 'first') -> Dict[str, Any]:
    

    missing: List[Dict[str, str]] = []
    if isinstance(left, str) and not os.path.exists(left):
        missing.append({'side': 'left', 'path': left})
    if isinstance(right, str) and not os.path.exists(right):
        missing.append({'side': 'right', 'path': right})

    if missing:
        return {
            'ok': False,
            'summary': 'missing input file(s)',
            'details': {
                'missing': missing,
                'warnings': [],
                'mismatches': [],
            }
        }


    l = _load_schema(left)
    r = _load_schema(right)

    lf = l.get('files') or []
    rf = r.get('files') or []

    reports: List[Dict[str, Any]] = []
    matched_pairs: List[str] = []
    unmatched_pairs: List[Dict[str, Any]] = []

    def run_pair(ls, rs):
        ok, det = _compare_single(ls, rs,
                                  compare=compare,
                                  case_sensitive=case_sensitive,
                                  order_sensitive=order_sensitive,
                                  relaxed_types=relaxed_types,
                                  nullable_strict=nullable_strict,
                                  pattern_mode=pattern_mode)
        return ok, det

    if not lf and not rf:
        ok, det = run_pair(l, r)
        reports.append(det)
        overall_ok = ok
    else:
        if lf and rf:
            rmap = {}
            for idx, item in enumerate(rf):
                fname = ((item.get('meta') or {}).get('file_name')) or f'idx:{idx}'
                rmap[fname] = item
            oks = []
            for idx, li in enumerate(lf):
                fname = ((li.get('meta') or {}).get('file_name')) or f'idx:{idx}'
                ri = rmap.get(fname)
                if ri is None:
                    unmatched_pairs.append({'left': fname, 'reason': 'no matching right'})
                    continue
                ok, det = run_pair(li, ri)
                reports.append(det)
                matched_pairs.append(fname)
                oks.append(ok)
            if dir_mode == 'first':
                overall_ok = oks[0] if oks else False
            elif dir_mode == 'any':
                overall_ok = any(oks) if oks else False
            else:  # 'all'
                overall_ok = all(oks) if oks else False
        else:
            multi = lf or rf
            single = r if lf else l
            oks = []
            for idx, item in enumerate(multi):
                ok, det = run_pair(item, single)
                reports.append(det)
                matched_pairs.append(((item.get('meta') or {}).get('file_name')) or f'idx:{idx}')
                oks.append(ok)
            if dir_mode == 'first':
                overall_ok = oks[0] if oks else False
            elif dir_mode == 'any':
                overall_ok = any(oks) if oks else False
            else:
                overall_ok = all(oks) if oks else False

    warnings: List[Dict[str, Any]] = []
    mismatches: List[Dict[str, Any]] = []
    field_summaries: List[Dict[str, Any]] = []
    for rep in reports:
        warnings.extend(rep.get('warnings', []))
        mismatches.extend(rep.get('mismatches', []))
        if 'field_summary' in rep:
            field_summaries.append(rep['field_summary'])

    result = {
        'ok': bool(overall_ok),
        'summary': 'success' if overall_ok else 'mismatch',
        'details': {
            'warnings': warnings,
            'mismatches': mismatches,
        }
    }

    # Include matched_pairs/unmatched_pairs ONLY for multi-file inputs
    if lf or rf:
        result['details']['matched_pairs'] = matched_pairs
        result['details']['unmatched_pairs'] = unmatched_pairs

    # Include aggregated field_summary for readability in single-file too
    if field_summaries:
        result['details']['field_summary'] = field_summaries[0] if len(field_summaries) == 1 else field_summaries

    return result


# --- Writer helper: standardized precedence and Path handling ---

def write_report(
    report: dict,
    fmt: str = 'txt',
    output_path: str | None = None,
    *,
    output_dir: str = '.',
    output_file: str | None = None,
    ensure_dir: bool = True,
) -> pathlib.Path:
    """
    Write a verification report (from verify_schema) to disk.

    Precedence:
      1) If output_path is provided:
           - If absolute: write exactly there.
           - If relative and output_dir != '.': write under output_dir / output_path.
           - Else: write under current dir / output_path.
      2) Else: write under output_dir / output_file (output_file required).
    """
    if output_path is not None:
        p = pathlib.Path(output_path)
        if not p.is_absolute() and (output_dir or '.') != '.':
            target = pathlib.Path(output_dir) / p
        else:
            target = p
        if ensure_dir:
            target.parent.mkdir(parents=True, exist_ok=True)
    else:
        if not output_file:
            raise ValueError('Provide either output_path or output_file.')
        target_dir = pathlib.Path(output_dir)
        if ensure_dir:
            target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / output_file

    fmt = (fmt or 'txt').lower()

    if fmt == 'json':
        target.write_text(json.dumps(report, indent=2), encoding='utf-8')
        return target

    if fmt == 'yaml':
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise RuntimeError('PyYAML is required for YAML output. Install with: pip install PyYAML') from e
        target.write_text(yaml.safe_dump(report, sort_keys=False), encoding='utf-8')
        return target

    if fmt == 'txt':
        ok = report.get('ok', False)
        details = report.get('details', {}) or {}
        lines: List[str] = []
        lines.append(f"Result: {'OK' if ok else 'MISMATCH'}")

        # Friendly summary in original order when available
        fs = details.get('field_summary')
        if isinstance(fs, dict):
            matched = fs.get('matched_fields') or []
            left_only = fs.get('left_only_fields') or []
            right_only = fs.get('right_only_fields') or []
            lines.append('Common fields (order as in left): ' + (', '.join(matched) if matched else '(none)'))
            lines.append('Left-only:   ' + (', '.join(left_only) if left_only else '(none)'))
            lines.append('Right-only:  ' + (', '.join(right_only) if right_only else '(none)'))

        mismatches = details.get('mismatches') or []
        if mismatches:
            lines.append('Mismatches:')
            for m in mismatches:
                lines.append(f'  - {m}')

        warnings = details.get('warnings') or []
        if warnings:
            lines.append('Warnings:')
            for w in warnings:
                lines.append(f'  - {w}')

        target.write_text('\n'.join(lines), encoding='utf-8')
        return target

    raise ValueError(f"Unsupported fmt: {fmt!r}")
