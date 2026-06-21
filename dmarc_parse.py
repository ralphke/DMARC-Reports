"""Parse DMARC aggregate XML reports into normalized CSV files for Power BI analysis."""

import io
import gzip
import zipfile
import datetime as dt
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd  # pylint: disable=import-error

INPUT_DIR = Path("./inbox")          # where your ZIP/XML files land (all folders recursively)
OUTPUT_DIR = Path("./data_dmarc")    # normalized output for Power BI
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def _to_int(x, default=None):
    """Convert value to integer, returning default on failure."""
    try:
        return int(x)
    except (ValueError, TypeError):
        return default

def _text(elem, path, default=None):
    """Extract text from XML element at given path, return default if not found."""
    node = elem.find(path)
    return node.text.strip() if node is not None and node.text else default

def _extract_report_metadata(root):
    """Extract report-level metadata from DMARC XML root."""
    return {
        "org_name": _text(root, "report_metadata/org_name"),
        "email": _text(root, "report_metadata/email"),
        "report_id": _text(root, "report_metadata/report_id"),
        "date_begin": _to_int(_text(root, "report_metadata/date_range/begin")),
        "date_end": _to_int(_text(root, "report_metadata/date_range/end")),
    }


def _extract_policy_published(root):
    """Extract policy published section from DMARC XML root."""
    return {
        "pol_domain": _text(root, "policy_published/domain"),
        "adkim": _text(root, "policy_published/adkim"),
        "aspf": _text(root, "policy_published/aspf"),
        "pol_p": _text(root, "policy_published/p"),
        "pol_sp": _text(root, "policy_published/sp"),
        "pol_pct": _to_int(_text(root, "policy_published/pct")),
    }


def _extract_row_fields(row_elem):
    """Extract row-level fields from DMARC record."""
    return {
        "source_ip": _text(row_elem, "source_ip"),
        "msg_count": _to_int(_text(row_elem, "count"), 0),
        "disp": _text(row_elem, "policy_evaluated/disposition"),
        "dkim_eval": _text(row_elem, "policy_evaluated/dkim"),
        "spf_eval": _text(row_elem, "policy_evaluated/spf"),
        "reason_type": _text(row_elem, "policy_evaluated/reason/type"),
        "reason_comm": _text(row_elem, "policy_evaluated/reason/comment"),
    }


def _extract_identifiers(rec):
    """Extract identifier fields from DMARC record."""
    return {
        "header_from": _text(rec, "identifiers/header_from"),
        "envelope_from": _text(rec, "identifiers/envelope_from"),
    }


def _extract_auth_results(rec):
    """Extract authentication results from DMARC record."""
    return {
        "dkim_domain": _text(rec, "auth_results/dkim/domain"),
        "dkim_result": _text(rec, "auth_results/dkim/result"),
        "dkim_selector": _text(rec, "auth_results/dkim/selector"),
        "spf_domain": _text(rec, "auth_results/spf/domain"),
        "spf_result": _text(rec, "auth_results/spf/result"),
        "spf_scope": _text(rec, "auth_results/spf/scope"),
    }


def _parse_record(rec, metadata, policy, source_file):
    """Parse a single DMARC record element into a row dictionary."""
    row_elem = rec.find("row")
    if row_elem is None:
        return None

    row_fields = _extract_row_fields(row_elem)
    identifiers = _extract_identifiers(rec)
    auth_results = _extract_auth_results(rec)

    date_begin = metadata["date_begin"]
    date_end = metadata["date_end"]

    return {
        "report_org": metadata["org_name"],
        "report_email": metadata["email"],
        "report_id": metadata["report_id"],
        "report_begin_utc": (
            dt.datetime.fromtimestamp(date_begin, dt.UTC) if date_begin else None
        ),
        "report_end_utc": (
            dt.datetime.fromtimestamp(date_end, dt.UTC) if date_end else None
        ),
        "policy_domain": policy["pol_domain"],
        "policy_adkim": policy["adkim"],
        "policy_aspf": policy["aspf"],
        "policy_p": policy["pol_p"],
        "policy_sp": policy["pol_sp"],
        "policy_pct": policy["pol_pct"],
        "source_ip": row_fields["source_ip"],
        "message_count": row_fields["msg_count"],
        "disposition": row_fields["disp"],
        "dkim_aligned": row_fields["dkim_eval"],
        "spf_aligned": row_fields["spf_eval"],
        "fail_reason_type": row_fields["reason_type"],
        "fail_reason_comment": row_fields["reason_comm"],
        "header_from": identifiers["header_from"],
        "envelope_from": identifiers["envelope_from"],
        "auth_dkim_domain": auth_results["dkim_domain"],
        "auth_dkim_result": auth_results["dkim_result"],
        "auth_dkim_selector": auth_results["dkim_selector"],
        "auth_spf_domain": auth_results["spf_domain"],
        "auth_spf_result": auth_results["spf_result"],
        "auth_spf_scope": auth_results["spf_scope"],
        "source_file": source_file,
    }


def parse_dmarc_xml(xml_bytes: bytes, source_file: str) -> pd.DataFrame:
    """
    Parses a single DMARC aggregate XML into a normalized pandas DataFrame.
    Schema focuses on the fields most useful for monitoring & security triage.
    """
    root = ET.fromstring(xml_bytes)

    metadata = _extract_report_metadata(root)
    policy = _extract_policy_published(root)

    rows = []
    for rec in root.findall("record"):
        row_data = _parse_record(rec, metadata, policy, source_file)
        if row_data:
            rows.append(row_data)

    df = pd.DataFrame(rows)

    # Convenience computed flags
    if not df.empty:
        df["dmarc_pass"] = (
            df["dkim_aligned"].eq("pass") | df["spf_aligned"].eq("pass")
        )
        df["both_fail"] = (
            df["dkim_aligned"].eq("fail") & df["spf_aligned"].eq("fail")
        )
    return df

def sniff_and_parse_file(path: Path) -> pd.DataFrame:
    """Detect file format (ZIP/GZIP/XML) and parse DMARC content."""
    with open(path, "rb") as f:
        raw = f.read()

    # ZIP file with one or more XMLs
    if zipfile.is_zipfile(io.BytesIO(raw)):
        out = []
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for name in z.namelist():
                if name.lower().endswith(".xml"):
                    xml_bytes = z.read(name)
                    out.append(
                        parse_dmarc_xml(xml_bytes, f"{path.name}:{name}")
                    )
        return pd.concat(out, ignore_index=True) if out else pd.DataFrame()

    # Gzip-compressed XML
    try:
        if raw[:2] == b"\x1f\x8b":
            xml_bytes = gzip.decompress(raw)
            return parse_dmarc_xml(xml_bytes, path.name)
    except (OSError, gzip.BadGzipFile):
        pass

    # Plain XML
    if path.suffix.lower() == ".xml":
        return parse_dmarc_xml(raw, path.name)

    return pd.DataFrame()

def main():
    """Main entry point: parse all DMARC files and generate CSV output."""
    all_rows = []
    for p in INPUT_DIR.glob("**/*"):
        if not p.is_file():
            continue
        if p.suffix.lower() in {".zip", ".gz", ".xml"}:
            try:
                df = sniff_and_parse_file(p)
                if not df.empty:
                    all_rows.append(df)
            except (ET.ParseError, ValueError, OSError) as e:
                print(f"Failed parsing {p}: {e}")

    if not all_rows:
        print("No DMARC rows parsed.")
        return

    df_all = pd.concat(all_rows, ignore_index=True)

    # Partitioned output by report_end date to aid incremental refresh
    df_all["report_date"] = pd.to_datetime(df_all["report_end_utc"]).dt.date
    for day, df_day in df_all.groupby("report_date"):
        out_path = OUTPUT_DIR / f"dmarc_{day}.csv"
        df_day.to_csv(out_path, index=False)
        print(f"Wrote {out_path} ({len(df_day)} rows)")

if __name__ == "__main__":
    main()
