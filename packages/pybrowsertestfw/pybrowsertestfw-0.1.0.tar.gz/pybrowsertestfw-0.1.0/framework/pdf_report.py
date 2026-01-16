import os
import re
import json
import time
import math
import sys
import platform
import io
import html
import ast
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPORTS_CURRENT_DIR: str | None = None
PYTEST_ROOT_DIR: str | None = None
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Image, Preformatted, KeepTogether
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.enums import TA_CENTER
    _REPORTLAB_AVAILABLE = True
except Exception:
    _REPORTLAB_AVAILABLE = False

class SimplePDF:
    def __init__(self, pagesize=(595.0, 842.0)):
        self.pagesize = pagesize
        self.pages = []
        self.title: str | None = None
        self._add_page()

    def _add_page(self):
        self.pages.append({"content": []})
        return len(self.pages) - 1

    def new_page(self):
        return self._add_page()

    def _escape(self, s: str) -> str:
        return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def set_fill_rgb(self, r, g, b):
        self.pages[-1]["content"].append(f"{r} {g} {b} rg")

    def set_stroke_rgb(self, r, g, b):
        self.pages[-1]["content"].append(f"{r} {g} {b} RG")

    def rect(self, x, y, w, h, fill=False, stroke=True):
        self.pages[-1]["content"].append(f"{x} {y} {w} {h} re")
        if fill and stroke:
            self.pages[-1]["content"].append("B")
        elif fill:
            self.pages[-1]["content"].append("f")
        elif stroke:
            self.pages[-1]["content"].append("S")

    def line(self, x1, y1, x2, y2):
        self.pages[-1]["content"].append(f"{x1} {y1} m")
        self.pages[-1]["content"].append(f"{x2} {y2} l")
        self.pages[-1]["content"].append("S")

    def text(self, x, y, s, size=12, color=(0,0,0), bold=False, mono=False):
        s = self._escape(s)
        self.pages[-1]["content"].append("BT")
        self.pages[-1]["content"].append(f"{color[0]} {color[1]} {color[2]} rg")
        font_tag = "F3" if mono else ("F2" if bold else "F1")
        self.pages[-1]["content"].append(f"/{font_tag} {size} Tf")
        self.pages[-1]["content"].append(f"{x} {y} Td")
        self.pages[-1]["content"].append(f"({s}) Tj")
        self.pages[-1]["content"].append("ET")

    def save(self, path):
        header = "%PDF-1.4\n"
        objects = []
        catalog_id = 1
        pages_id = 2
        font_id = 3
        objects.append((catalog_id, f"<< /Type /Catalog /Pages {pages_id} 0 R >>"))
        objects.append((font_id, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"))
        font_bold_id = font_id + 1
        objects.append((font_bold_id, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"))
        font_mono_id = font_bold_id + 1
        objects.append((font_mono_id, "<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>"))
        info_id = font_mono_id + 1
        title = self.title or os.path.basename(path) or "Test Execution Report"
        title_escaped = self._escape(str(title))
        objects.append((info_id, f"<< /Title ({title_escaped}) >>"))
        first_page_id = info_id + 1
        page_object_ids = []
        content_ids = []
        for i in range(len(self.pages)):
            pid = first_page_id + i * 2
            cid = pid + 1
            page_object_ids.append(pid)
            content_ids.append(cid)
        kids = " ".join([f"{i} 0 R" for i in page_object_ids])
        objects.append((pages_id, f"<< /Type /Pages /Kids [{kids}] /Count {len(page_object_ids)} >>"))
        for idx, page in enumerate(self.pages):
            pid = page_object_ids[idx]
            cid = content_ids[idx]
            objects.append((pid, f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {self.pagesize[0]} {self.pagesize[1]}] /Resources << /Font << /F1 {font_id} 0 R /F2 {font_bold_id} 0 R /F3 {font_mono_id} 0 R >> >> /Contents {cid} 0 R >>"))
            stream = "\n".join(page["content"]) + "\n"
            length = len(stream.encode("latin-1", "ignore"))
            content = f"<< /Length {length} >>\nstream\n{stream}endstream"
            objects.append((cid, content))
        parts = [header]
        offsets = []
        for oid, body in objects:
            offsets.append(sum(len(p.encode("latin-1", "ignore")) for p in parts))
            parts.append(f"{oid} 0 obj\n{body}\nendobj\n")
        xref_offset = sum(len(p.encode("latin-1", "ignore")) for p in parts)
        count = len(objects) + 1
        xref = ["xref\n", f"0 {count}\n", "0000000000 65535 f \n"]
        for off in offsets:
            xref.append(f"{off:010d} 00000 n \n")
        trailer = f"trailer\n<< /Size {count} /Root {catalog_id} 0 R /Info {info_id} 0 R >>\nstartxref\n{xref_offset}\n%%EOF"
        parts.extend(xref)
        parts.append(trailer)
        data = "".join(parts).encode("latin-1", "ignore")
        with open(path, "wb") as f:
            f.write(data)

def _find_latest_report_paths(base_dir: str):
    latest = None
    html = None
    js = None
    if not os.path.isdir(base_dir):
        return None
    items = []
    for name in os.listdir(base_dir):
        p = os.path.join(base_dir, name)
        if os.path.isdir(p):
            items.append((name, p))
    items.sort(key=lambda x: x[0], reverse=True)
    for name, p in items:
        h = None
        j = None
        for fn in os.listdir(p):
            if fn.endswith(".html") and fn.startswith("report_"):
                h = os.path.join(p, fn)
            if fn.endswith(".json") and fn.startswith("report_"):
                j = os.path.join(p, fn)
        if h and j:
            latest = p
            html = h
            js = j
            break
    if not latest:
        return None
    return {"dir": latest, "html": html, "json": js}

def _parse_html_env(html_path: str):
    env = {}
    if not html_path or not os.path.isfile(html_path):
        return env
    try:
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        m = re.search(r'data-jsonblob="([^"]+)"', txt)
        if not m:
            return env
        raw = m.group(1)
        raw = raw.replace("&#34;", '"')
        data = json.loads(raw)
        return data.get("environment", {})
    except Exception:
        return env

def _parse_html_blob(html_path: str):
    blob = {}
    if not html_path or not os.path.isfile(html_path):
        return blob
    try:
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        m = re.search(r'data-jsonblob="([^"]+)"', txt)
        if not m:
            return blob
        raw = m.group(1).replace("&#34;", '"')
        blob = json.loads(raw)
    except Exception:
        return {}
    return blob

def _parse_json(json_path: str):
    data = {}
    if not json_path or not os.path.isfile(json_path):
        return data
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    return data

def _build_summary(json_data):
    tests = json_data.get("tests", []) or []
    summary_meta = json_data.get("summary", {}) or {}
    if tests:
        total = len(tests)
        passed = 0
        failed = 0
        skipped = 0
        for t in tests:
            oc = _normalize_outcome_for_view(t.get("outcome"))
            if oc == "passed":
                passed += 1
            elif oc == "failed":
                failed += 1
            elif oc == "skipped":
                skipped += 1
    else:
        total = summary_meta.get("total", 0)
        passed = summary_meta.get("passed", 0)
        failed = summary_meta.get("failed", 0)
        skipped = summary_meta.get("skipped", 0)
    duration = json_data.get("duration") or 0
    created = json_data.get("created") or time.time()
    start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created))
    end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created + duration))
    rate = 0.0
    if total:
        rate = passed * 100.0 / total
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "duration": duration,
        "period": f"{start} to {end}",
        "pass_rate": rate,
    }

def _fmt_duration(value) -> str:
    try:
        s = float(value)
    except Exception:
        return str(value)
    if s >= 0 and s < 1.0:
        ms = int(round(s * 1000.0))
        return f"{ms}ms"
    secs = int(s)
    return f"{secs}s"

def _normalize_outcome_for_view(oc) -> str:
    try:
        s = str(oc).lower()
    except Exception:
        return "unknown"
    if s == "error":
        return "failed"
    return s

def _extract_mn_tags(t: dict) -> list[str]:
    tags: set[str] = set()
    try:
        kw = t.get("keywords")
        if isinstance(kw, dict):
            for k, v in kw.items():
                if isinstance(k, str) and str(k).startswith("MN_") and bool(v):
                    tags.add(str(k))
        elif isinstance(kw, list):
            for it in kw:
                name = None
                if isinstance(it, str):
                    name = it
                elif isinstance(it, dict):
                    name = it.get("name") or it.get("marker") or it.get("id")
                if isinstance(name, str) and name.startswith("MN_"):
                    tags.add(name)
        mr = t.get("markers")
        if isinstance(mr, list):
            for it in mr:
                name = None
                if isinstance(it, str):
                    name = it
                elif isinstance(it, dict):
                    name = it.get("name") or it.get("marker") or it.get("id")
                if isinstance(name, str) and name.startswith("MN_"):
                    tags.add(name)
    except Exception:
        pass
    return sorted(tags)

def _strip_mn(tag: str) -> str:
    try:
        return tag[3:] if tag.startswith("MN_") else tag
    except Exception:
        return tag

def _add_marker_from_line(line: str, mn_list: list[str]) -> None:
    try:
        s = line.strip()
        if not s or s.startswith("#"):
            return
        head = s.split(":", 1)[0].strip()
        if head.startswith("MN_") and head not in mn_list:
            mn_list.append(head)
    except Exception:
        return

def _load_module_tags_from_pytest_ini() -> list[str]:
    mn_list: list[str] = []
    search_dirs: list[str] = []
    try:
        if REPORTS_CURRENT_DIR:
            search_dirs.append(os.path.abspath(REPORTS_CURRENT_DIR))
    except Exception:
        pass
    search_dirs.append(PROJECT_ROOT)
    ini_path = None
    seen: set[str] = set()
    for base in search_dirs:
        cur = os.path.abspath(base)
        while cur and cur not in seen:
            seen.add(cur)
            cand = os.path.join(cur, "pytest.ini")
            if os.path.isfile(cand):
                ini_path = cand
                break
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
        if ini_path:
            break
    if not ini_path:
        return mn_list
    global PYTEST_ROOT_DIR
    PYTEST_ROOT_DIR = os.path.dirname(ini_path)
    in_markers = False
    try:
        with open(ini_path, "r", encoding="utf-8", errors="ignore") as f:
            for raw in f:
                line = raw.rstrip("\n")
                stripped = line.strip()
                lower = stripped.lower()
                if lower.startswith("[") and "]" in lower:
                    in_markers = False
                if lower.startswith("markers"):
                    in_markers = True
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        _add_marker_from_line(parts[1], mn_list)
                    continue
                if in_markers:
                    _add_marker_from_line(line, mn_list)
    except Exception:
        return mn_list
    return mn_list
def _extract_marker_names_from_node(node) -> set[str]:
    names: set[str] = set()
    if node is None:
        return names
    try:
        if isinstance(node, ast.Constant):
            v = node.value
            if isinstance(v, str) and v.startswith("MN_"):
                names.add(v)
        if isinstance(node, ast.Name):
            n = node.id
            if isinstance(n, str) and n.startswith("MN_"):
                names.add(n)
        elif isinstance(node, ast.Attribute):
            attr = node.attr
            if isinstance(attr, str) and attr.startswith("MN_"):
                names.add(attr)
            names |= _extract_marker_names_from_node(node.value)
        elif isinstance(node, ast.Call):
            names |= _extract_marker_names_from_node(node.func)
            for a in node.args:
                names |= _extract_marker_names_from_node(a)
            for kw in node.keywords:
                names |= _extract_marker_names_from_node(kw.value)
        elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            for e in node.elts:
                names |= _extract_marker_names_from_node(e)
        elif isinstance(node, ast.Dict):
            for v in node.values:
                names |= _extract_marker_names_from_node(v)
        elif isinstance(node, ast.UnaryOp):
            names |= _extract_marker_names_from_node(node.operand)
        elif isinstance(node, ast.BinOp):
            names |= _extract_marker_names_from_node(node.left)
            names |= _extract_marker_names_from_node(node.right)
    except Exception:
        return names
    return names

def _extract_marker_names_from_decorators(decos) -> set[str]:
    names: set[str] = set()
    try:
        for d in decos or []:
            names |= _extract_marker_names_from_node(d)
    except Exception:
        return names
    return names

def _scan_module_case_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    base_root = PYTEST_ROOT_DIR or PROJECT_ROOT
    tests_root = os.path.join(base_root, "tests")
    if not os.path.isdir(tests_root):
        return counts
    try:
        for dirpath, _, filenames in os.walk(tests_root):
            for fn in filenames:
                if not fn.endswith(".py") or not fn.startswith("test_"):
                    continue
                fpath = os.path.join(dirpath, fn)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        src = f.read()
                    tree = ast.parse(src, filename=fpath)
                except Exception:
                    continue
                module_marks: set[str] = set()
                for node in getattr(tree, "body", []):
                    if isinstance(node, (ast.Assign, ast.AnnAssign)):
                        targets = []
                        value = None
                        if isinstance(node, ast.Assign):
                            targets = node.targets
                            value = node.value
                        else:
                            targets = [node.target]
                            value = node.value
                        for t in targets:
                            if isinstance(t, ast.Name) and t.id == "pytestmark":
                                module_marks |= _extract_marker_names_from_node(value)

                def visit(node, inherited_marks: set[str]):
                    if isinstance(node, ast.ClassDef):
                        class_marks = inherited_marks | _extract_marker_names_from_decorators(node.decorator_list)
                        for child in node.body:
                            visit(child, class_marks)
                        return
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        func_marks = inherited_marks | _extract_marker_names_from_decorators(node.decorator_list)
                        mn_found = {m for m in func_marks if m.startswith("MN_")}
                        if not mn_found:
                            return
                        for m in mn_found:
                            counts[m] = counts.get(m, 0) + 1
                        return
                    for child in ast.iter_child_nodes(node):
                        visit(child, inherited_marks)

                base_marks = module_marks
                for node in getattr(tree, "body", []):
                    visit(node, base_marks)
    except Exception:
        return counts
    return counts

def _group_by_module(json_data):
    mods: dict[str, dict] = {}
    mn_ini = _load_module_tags_from_pytest_ini()
    for raw_mn in mn_ini:
        if not raw_mn:
            continue
        mn_name = _strip_mn(raw_mn)
        mods[raw_mn] = {"id": "", "name": mn_name, "passed": 0, "failed": 0, "skipped": 0, "cases": 0}
    tests = json_data.get("tests", [])
    for t in tests:
        oc = _normalize_outcome_for_view(t.get("outcome"))
        raw_mn = _extract_mn_tags(t)
        if not raw_mn:
            continue
        seen: set[str] = set()
        for tag in raw_mn:
            if not tag or tag in seen:
                continue
            seen.add(tag)
            name = _strip_mn(tag)
            d = mods.setdefault(tag, {"id": "", "name": name, "passed": 0, "failed": 0, "skipped": 0, "cases": 0})
            d["cases"] += 1
            if oc == "passed":
                d["passed"] += 1
            elif oc == "failed":
                d["failed"] += 1
            elif oc == "skipped":
                d["skipped"] += 1
    defined_counts = _scan_module_case_counts()
    for key, d in mods.items():
        defined_total = 0
        if key in defined_counts:
            defined_total = defined_counts[key]
        else:
            mn_key = "MN_" + d.get("name", "") if d.get("name") else ""
            if mn_key and mn_key in defined_counts:
                defined_total = defined_counts[mn_key]
        if defined_total > d["cases"]:
            extra = defined_total - d["cases"]
            d["cases"] = defined_total
            d["skipped"] += extra
    filtered: dict[str, dict] = {}
    for key, d in mods.items():
        mid = d.get("id") or ""
        mname = d.get("name") or ""
        if mid and not mname:
            continue
        filtered[key] = d
    return filtered

def _case_rows(json_data):
    rows = []
    tests = json_data.get("tests", [])
    for idx, t in enumerate(tests, start=1):
        nid = t.get("nodeid", "")
        parts = nid.split("::")
        suite = parts[0] if parts else "tests"
        try:
            s = suite.replace("\\", "/")
            if s.startswith("tests/"):
                suite = s[6:]
            else:
                suite = s
        except Exception:
            pass
        case = parts[1] if len(parts) > 1 else nid
        oc = _normalize_outcome_for_view(t.get("outcome"))
        dur = 0.0
        for k in ("setup", "call", "teardown"):
            if isinstance(t.get(k), dict):
                d = t[k].get("duration")
                if isinstance(d, (int, float)):
                    dur += d
        rows.append([str(idx), suite, case, oc.capitalize(), _fmt_duration(dur)])
    return rows

def _collect_detail(json_data, html_blob=None):
    details = []
    tests = json_data.get("tests", [])
    for t in tests:
        nid = t.get("nodeid", "")
        parts = nid.split("::")
        suite = parts[0] if parts else "tests"
        try:
            s = suite.replace("\\", "/")
            if s.startswith("tests/"):
                suite = s[6:]
            else:
                suite = s
        except Exception:
            pass
        case = parts[1] if len(parts) > 1 else nid
        oc_raw = t.get("outcome")
        dur = 0.0
        logs = []
        has_error = False
        for k in ("setup", "call", "teardown"):
            sec = t.get(k) or {}
            d = sec.get("duration")
            if isinstance(d, (int, float)):
                dur += d
            for log in sec.get("log", [])[:20]:
                msg = log.get("msg") if isinstance(log, dict) else str(log)
                lvl = log.get("levelname") if isinstance(log, dict) else None
                if msg:
                    logs.append(str(msg))
                if isinstance(lvl, str) and lvl.upper() in ("ERROR", "CRITICAL"):
                    has_error = True
        if isinstance(oc_raw, str) and oc_raw.lower() in ("failed", "error"):
            has_error = True
        err_text = ""
        # Prefer HTML blob's per-test log if available
        try:
            if html_blob and isinstance(html_blob.get("tests"), dict):
                items = html_blob["tests"].get(nid) or []
                if items:
                    log_str = items[0].get("log") or ""
                    log_str = _html_unescape_multi(log_str)
                    if log_str:
                        m = re.search(r"FAILURES[\s\S]*?(?=Captured log setup)", log_str, flags=re.IGNORECASE)
                        if m:
                            err_text = m.group(0)
                        else:
                            lines_e = re.findall(r"^E.*$", log_str, flags=re.MULTILINE)
                            if lines_e:
                                err_text = "\n".join(lines_e[:12])
        except Exception:
            pass
        if not err_text:
            # Fallback to JSON longrepr if present
            try:
                call = t.get("call") or {}
                lr = call.get("longrepr")
                lr_text = ""
                if isinstance(lr, str):
                    lr_text = lr
                elif isinstance(lr, dict):
                    ent = lr.get("reprtraceback", {}).get("entries", [])
                    if isinstance(ent, list):
                        lr_text = "\n".join([e.get("data", "") for e in ent if isinstance(e, dict)])
                    lr_text = lr_text or lr.get("reprcrash", {}).get("message", "")
                if lr_text:
                    lr_text = _html_unescape_multi(lr_text)
                    m2 = re.search(r"FAILURES[\s\S]*?(?=Captured log setup)", lr_text, flags=re.IGNORECASE)
                    err_text = m2.group(0) if m2 else lr_text
            except Exception:
                pass
        if not err_text and logs:
            err_text = "\n".join([ln for ln in logs if ln][:10])
        err_text = _cleanup_err_text(_post_err(err_text, t))
        shots = []
        for p in t.get("screenshots", []) or []:
            try:
                candidates = []
                if os.path.isabs(p):
                    candidates.append(p)
                else:
                    candidates.append(os.path.abspath(p))
                    candidates.append(os.path.abspath(os.path.join(PROJECT_ROOT, p)))
                for pp in candidates:
                    if os.path.isfile(pp):
                        shots.append(pp)
                        break
            except Exception:
                pass
        env = {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Python": sys.version.split()[0],
        }
        oc_view = _normalize_outcome_for_view(oc_raw)
        details.append({
            "suite": suite,
            "case": case,
            "status": oc_view.capitalize(),
            "duration": _fmt_duration(dur),
            "logs": logs,
            "has_error": has_error,
            "screenshots": shots,
            "error_message": err_text,
            "env": env,
        })
    return details

def _draw_table(pdf: SimplePDF, x, y, col_widths, row_height, rows, header=False, header_fill=(0.95,0.95,0.95), zebra=False, result_col=None):
    cur_y = y
    if header and rows:
        pdf.set_fill_rgb(*header_fill)
        pdf.rect(x, cur_y - row_height, sum(col_widths), row_height, fill=True, stroke=False)
        pdf.set_stroke_rgb(0,0,0)
        pdf.rect(x, cur_y - row_height, sum(col_widths), row_height, fill=False, stroke=True)
        cx = x + 4
        for i, w in enumerate(col_widths):
            pdf.text(cx, cur_y - row_height + 6, rows[0][i], 10, (0,0,0), bold=True)
            cx += w
        cur_y -= row_height
        rows = rows[1:]
    idx = 0
    for r in rows:
        if zebra and idx % 2 == 1:
            pdf.set_fill_rgb(0.985,0.985,0.985)
            pdf.rect(x, cur_y - row_height, sum(col_widths), row_height, fill=True, stroke=False)
        pdf.set_stroke_rgb(0,0,0)
        pdf.rect(x, cur_y - row_height, sum(col_widths), row_height, fill=False, stroke=True)
        cx = x + 4
        for i, w in enumerate(col_widths):
            txt = r[i]
            if result_col is not None and i == result_col:
                t = txt.lower()
                col = (0,0,0)
                if "passed" in t:
                    col = (0.2,0.6,0.2)
                elif "failed" in t:
                    col = (0.85,0.2,0.2)
                elif "skipped" in t:
                    col = (0.8,0.5,0.0)
                pdf.text(cx, cur_y - row_height + 6, txt[:200], 10, col)
            else:
                try:
                    max_chars = max(3, int((w - 8) / 6))
                except Exception:
                    max_chars = 32
                out = txt
                if isinstance(out, str) and len(out) > max_chars:
                    out = out[:max_chars-1] + "…"
                pdf.text(cx, cur_y - row_height + 6, out, 10, (0,0,0))
            cx += w
        cur_y -= row_height
        idx += 1
    return cur_y

def generate_pdf_report(template_path=None, html_path=None, json_path=None, output_pdf_path=None, execution_mode="PyTest"):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    reports_dir = os.path.join(base, "reports")
    if not html_path or not json_path:
        latest = _find_latest_report_paths(reports_dir)
        if latest:
            html_path = html_path or latest["html"]
            json_path = json_path or latest["json"]
    global REPORTS_CURRENT_DIR
    REPORTS_CURRENT_DIR = os.path.dirname(html_path or json_path or reports_dir)
    data = _parse_json(json_path) if json_path else {}
    env = _parse_html_env(html_path) if html_path else {}
    html_blob = _parse_html_blob(html_path) if html_path else {}
    summary = _build_summary(data)
    python_ver = sys.version.split()[0]
    mods = _group_by_module(data)
    case_rows = _case_rows(data)
    details = _collect_detail(data, html_blob)
    def _extract_ts_from_path(p: str | None) -> str | None:
        try:
            if not p:
                return None
            m = re.search(r"report_(\d{8}_\d{6})\.(?:html|json)$", os.path.basename(p))
            return m.group(1) if m else None
        except Exception:
            return None

    out_path = output_pdf_path
    if not out_path:
        ts = _extract_ts_from_path(html_path) or _extract_ts_from_path(json_path) or time.strftime("%Y%m%d_%H%M%S")
        out_dir = os.path.dirname(json_path or html_path or os.path.join(reports_dir, ts))
        out_dir = os.path.abspath(out_dir)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"report_{ts}.pdf")
    REPORTS_CURRENT_DIR = os.path.dirname(html_path or json_path or out_path)
    shots_dir = os.path.join(REPORTS_CURRENT_DIR, "screenshot") if REPORTS_CURRENT_DIR else None
    screenshots_all = []
    try:
        if shots_dir and os.path.isdir(shots_dir):
            for fn in sorted(os.listdir(shots_dir)):
                if fn.lower().endswith((".png", ".jpg", ".jpeg")):
                    screenshots_all.append(os.path.join(shots_dir, fn))
    except Exception:
        pass

    if _REPORTLAB_AVAILABLE:
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, textColor=colors.black, spaceAfter=12)
        h_style = ParagraphStyle("h", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14, textColor=colors.black, spaceBefore=10, spaceAfter=6)
        body_style = ParagraphStyle("body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10, leading=12, textColor=colors.black)
        small_style = ParagraphStyle("small", parent=styles["BodyText"], fontName="Helvetica", fontSize=9, leading=10, textColor=colors.black)
        cell_wrap_style = ParagraphStyle("cellwrap", parent=small_style, wordWrap="CJK", spaceBefore=0, spaceAfter=0)
        mono_style = ParagraphStyle("mono", parent=styles["Code"], fontName="Courier", fontSize=9, leading=11, textColor=colors.black)
        err_pre_style = ParagraphStyle("errpre", parent=styles["BodyText"], fontName="Helvetica", fontSize=9, leading=10, alignment=TA_CENTER, textColor=colors.black)
        err_pre_style_err = ParagraphStyle("errpreerr", parent=err_pre_style, textColor=colors.Color(0.85,0.2,0.2))

        doc = SimpleDocTemplate(
            out_path,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36,
            title=os.path.basename(out_path) if out_path else "Test Execution Report",
        )
        content_width = A4[0] - doc.leftMargin - doc.rightMargin
        story = []
        story.append(Paragraph("Test Execution Report", title_style))
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        story.append(Paragraph(f"Generated: {ts}", small_style))
        story.append(Paragraph(f"Version: {python_ver}", small_style))
        pr = int(round(summary.get("pass_rate", 0)))
        total = summary.get("total", 0) or 1
        passed = summary.get("passed", 0)
        failed = summary.get("failed", 0)
        bar_w = int(content_width)
        pass_w = int(bar_w * (passed/total))
        fail_w = int(bar_w * (failed/total))
        rest_w = bar_w - pass_w - fail_w
        cells = []
        widths = []
        styles_bar = [("BOX", (0,0), (-1,-1), 0.5, colors.black)]
        idx = 0
        if pass_w > 0:
            cells.append("")
            widths.append(pass_w)
            styles_bar.append(("BACKGROUND", (idx,0), (idx,0), colors.Color(0.25,0.7,0.35)))
            idx += 1
        if fail_w > 0:
            cells.append("")
            widths.append(fail_w)
            styles_bar.append(("BACKGROUND", (idx,0), (idx,0), colors.Color(0.85,0.2,0.2)))
            idx += 1
        if rest_w > 0:
            cells.append("")
            widths.append(rest_w)
            styles_bar.append(("BACKGROUND", (idx,0), (idx,0), colors.Color(0.92,0.92,0.92)))
        if not cells:
            cells = [""]
            widths = [bar_w]
        bar_tbl = Table([cells], colWidths=widths, rowHeights=[10])
        bar_tbl.setStyle(TableStyle(styles_bar))
        story.append(Spacer(1, 6))
        story.append(bar_tbl)
        story.append(Paragraph(f"Pass rate: {pr}%", body_style))
        story.append(Spacer(1, 12))

        story.append(Paragraph("1 Summary", h_style))
        summary_rows = [["Execution Period", summary["period"]], ["Total", str(summary["total"])], ["Passed", str(summary["passed"])], ["Failed", str(summary["failed"])], ["Duration", _fmt_duration(summary["duration"])]]
        tbl = Table(summary_rows, colWidths=[170, content_width - 170])
        tbl.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.25, colors.black),
            ("TEXTCOLOR", (0,0), (0,-1), colors.black),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 10))

        story.append(Paragraph("2 Test Result Summary", h_style))
        header = ["Module Name", "Passed", "Failed", "Skipped", "Total", "Coverage"]
        rows2 = [header]
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        total_cases = 0
        sorted_mods = sorted(mods.values(), key=lambda d: (d.get("name") or ""))
        for v in sorted_mods:
            cov_str = "0%"
            if v["cases"]:
                cov_pct = (v["passed"] / v["cases"]) * 100.0
                cov_str = _fmt_pct(cov_pct)
            mname = v.get("name") or ""
            label = html.escape(mname) if mname else ""
            rows2.append([
                Paragraph(label, cell_wrap_style),
                Paragraph(str(v["passed"]), cell_wrap_style),
                Paragraph(str(v["failed"]), cell_wrap_style),
                Paragraph(str(v["skipped"]), cell_wrap_style),
                Paragraph(str(v["cases"]), cell_wrap_style),
                Paragraph(cov_str, cell_wrap_style),
            ])
            total_passed += int(v["passed"])
            total_failed += int(v["failed"])
            total_skipped += int(v["skipped"])
            total_cases += int(v["cases"])
        total_cov_str = "0%"
        if total_cases:
            total_cov_pct = (total_passed / total_cases) * 100.0
            total_cov_str = _fmt_pct(total_cov_pct)
        rows2.append([
            Paragraph("Total", cell_wrap_style),
            Paragraph(str(total_passed), cell_wrap_style),
            Paragraph(str(total_failed), cell_wrap_style),
            Paragraph(str(total_skipped), cell_wrap_style),
            Paragraph(str(total_cases), cell_wrap_style),
            Paragraph(total_cov_str, cell_wrap_style),
        ])
        name_w = int(content_width * 0.40)
        rest_w = content_width - name_w
        even_w = rest_w / 5.0
        tbl2 = Table(rows2, colWidths=[name_w, even_w, even_w, even_w, even_w, even_w])
        tbl2.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.25, colors.black),
            ("BACKGROUND", (0,0), (-1,0), colors.Color(0.95,0.95,0.95)),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ]))
        story.append(tbl2)
        story.append(Spacer(1, 10))

        story.append(Paragraph("3 Test Result", h_style))
        header3 = ["", "Test file", "Test Case", "Result", "Duration"]
        rows3 = [header3]
        for r in case_rows:
            rows3.append([r[0], Paragraph(r[1], cell_wrap_style), Paragraph(r[2], cell_wrap_style), r[3], r[4]])
        tbl3 = Table(rows3, colWidths=[int(content_width*0.07), int(content_width*0.33), int(content_width*0.38), int(content_width*0.12), int(content_width*0.10)])
        styles3 = [
            ("GRID", (0,0), (-1,-1), 0.25, colors.black),
            ("BACKGROUND", (0,0), (-1,0), colors.Color(0.95,0.95,0.95)),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ]
        for r in range(1, len(rows3)):
            if r % 2 == 0:
                styles3.append(("BACKGROUND", (0,r), (-1,r), colors.Color(0.985,0.985,0.985)))
            res = rows3[r][3].lower()
            if "passed" in res:
                styles3.append(("TEXTCOLOR", (3,r), (3,r), colors.Color(0.2,0.6,0.2)))
            elif "failed" in res:
                styles3.append(("TEXTCOLOR", (3,r), (3,r), colors.Color(0.85,0.2,0.2)))
            elif "skipped" in res:
                styles3.append(("TEXTCOLOR", (3,r), (3,r), colors.Color(0.8,0.5,0.0)))
        tbl3.setStyle(TableStyle(styles3))
        story.append(tbl3)
        story.append(Spacer(1, 10))

        story.append(Paragraph("4 Detail Result", h_style))
        groups: dict[str, list[dict]] = {}
        for d in details:
            s = (d.get("suite") or "").replace("\\", "/")
            if "/" in s:
                folder = os.path.basename(os.path.dirname(s))
            else:
                folder = "tests"
            groups.setdefault(folder, []).append(d)
        folder_idx = 1
        for folder, items in groups.items():
            para_folder = Paragraph(f"4.{folder_idx} Test folder: {folder}", ParagraphStyle("casef", parent=body_style, fontSize=12, fontName="Helvetica-Bold"))
            story.append(para_folder)
            file_idx = 1
            for d in items:
                file_name = os.path.basename((d.get("suite") or "").replace("\\", "/"))
                para_file = Paragraph(f"4.{folder_idx}.{file_idx} Test file: {file_name}", ParagraphStyle("casec", parent=body_style, fontSize=12, fontName="Helvetica-Bold"))
                para_case = Paragraph(f"Test case: {d['case']}", ParagraphStyle("caseline", parent=body_style, fontSize=11, fontName="Helvetica-Bold"))
                spacer_head = Spacer(1, 6)
                grid = [["Status", d["status"]], ["Test file", Paragraph(d["suite"], cell_wrap_style)], ["Test Case", Paragraph(d["case"], cell_wrap_style)], ["Timestamps", summary["period"].split(" to ")[0]]]
                err_text = d.get("error_message") if d.get("has_error") else ""
                imgs = [p for p in (d.get("screenshots", []) or []) if os.path.isfile(p)]
                grid.append(["Duration", d["duration"]])
                if imgs:
                    col2_w = int(content_width * 0.78)
                    target_w = int(col2_w - 8)
                    first = True
                    for p in imgs:
                        label = "Screen Capture(s)" if first else ""
                        first = False
                        try:
                            ir = ImageReader(p)
                            iw, ih = ir.getSize()
                            scale = target_w / float(iw) if iw else 1.0
                            target_h = int(ih * scale)
                            img_flow = Image(p, width=target_w, height=target_h)
                            grid.append([label, img_flow])
                        except Exception:
                            grid.append([label, Paragraph(os.path.basename(p), small_style)])
                else:
                    grid.append(["Screen Capture(s)", "No Screen Capture Provided"])
                tblg = Table(grid, colWidths=[int(content_width*0.22), int(content_width*0.78)])
                gstyle = [("GRID", (0,0), (-1,-1), 0.25, colors.black), ("TEXTCOLOR", (0,0), (0,-1), colors.black)]
                gstyle.append(("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"))
                gstyle.append(("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"))
                sc_start = None
                for i, r in enumerate(grid):
                    if r[0] == "Screen Capture(s)" or sc_start is not None:
                        sc_start = i if sc_start is None else sc_start
                if sc_start is not None:
                    gstyle.append(("VALIGN", (0, sc_start), (0, len(grid)-1), "TOP"))
                    gstyle.append(("VALIGN", (1, sc_start), (1, len(grid)-1), "TOP"))
                gstyle.append(("VALIGN", (1,0), (1,-1), "TOP"))
                t = d["status"].lower()
                if "passed" in t:
                    gstyle.append(("TEXTCOLOR", (1,0), (1,0), colors.Color(0.2,0.6,0.2)))
                elif "failed" in t:
                    gstyle.append(("TEXTCOLOR", (1,0), (1,0), colors.Color(0.85,0.2,0.2)))
                elif "skipped" in t:
                    gstyle.append(("TEXTCOLOR", (1,0), (1,0), colors.Color(0.8,0.5,0.0)))
                elif "error" in t:
                    gstyle.append(("TEXTCOLOR", (1,0), (1,0), colors.Color(0.85,0.2,0.2)))
                tblg.setStyle(TableStyle(gstyle))
                story.append(KeepTogether([para_file, para_case, spacer_head, tblg]))
                if t in ("failed", "error") and err_text:
                    story.append(Spacer(1, 6))
                    story.append(Paragraph("Error Message:", ParagraphStyle("emh", parent=body_style, fontName="Helvetica-Bold")))
                    story.append(Spacer(1, 10))
                    block_w = int(content_width)
                    inner_w = int(content_width - 16)
                    wrapped = _wrap_error_text(err_text, inner_w, font_name="Helvetica", font_size=9)
                    lines = wrapped.split("\n")
                    code_rows = []
                    for ln in lines:
                        txt = ln if ln else " "
                        style = err_pre_style_err
                        code_rows.append([Preformatted(txt, style)])
                    code_table = Table(code_rows, colWidths=[inner_w])
                    code_table.hAlign = "LEFT"
                    code_table.setStyle(TableStyle([
                        ("BACKGROUND", (0,0), (-1,-1), colors.Color(0.965,0.965,0.965)),
                        ("BOX", (0,0), (-1,-1), 0.5, colors.Color(0.75,0.75,0.75)),
                        ("LEFTPADDING", (0,0), (-1,-1), 6),
                        ("RIGHTPADDING", (0,0), (-1,-1), 6),
                        ("TOPPADDING", (0,0), (-1,-1), 6),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                        ("ALIGN", (0,0), (-1,-1), "CENTER"),
                    ]))
                    story.append(code_table)
                story.append(Spacer(1, 8))
                file_idx += 1
            folder_idx += 1

        try:
            doc.build(story)
        except Exception:
            pass
        return out_path

    pdf = SimplePDF()
    w, h = pdf.pagesize
    y = h - 40
    cw = w - 80
    pdf.text(40, y, "Test Execution Report", 18, (0.1,0.1,0.1), bold=True)
    y -= 22
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    pdf.text(40, y, f"Generated: {ts}", 10, (0.2,0.2,0.2))
    y -= 14
    pdf.text(40, y, f"Version: {python_ver}", 10, (0.2,0.2,0.2))
    y -= 20
    pr = int(round(summary.get("pass_rate", 0)))
    total = summary.get("total", 0) or 1
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    pdf.text(40, y+10, f"Pass rate: {pr}%", 10, (0.1,0.1,0.1))
    pdf.set_fill_rgb(0.92,0.92,0.92)
    pdf.rect(40, y, cw, 8, fill=True, stroke=False)
    pw = cw * (passed/total)
    fw = cw * (failed/total)
    if pw > 0:
        pdf.set_fill_rgb(0.25,0.7,0.35)
        pdf.rect(40, y, pw, 8, fill=True, stroke=False)
    if fw > 0:
        pdf.set_fill_rgb(0.85,0.2,0.2)
        pdf.rect(40 + pw, y, fw, 8, fill=True, stroke=False)
    pdf.set_stroke_rgb(0,0,0)
    pdf.rect(40, y, cw, 8, fill=False, stroke=True)
    y -= 28
    pdf.text(40, y, "1 Summary", 14, (0.1,0.1,0.1), bold=True)
    y -= 18
    rows = [["Execution Period", summary["period"]], ["Total", str(summary["total"])], ["Passed", str(summary["passed"])], ["Failed", str(summary["failed"])], ["Duration", _fmt_duration(summary["duration"])]]
    colw = [150, cw - 150]
    for r in rows:
        pdf.rect(40, y-18, sum(colw), 18, fill=False, stroke=True)
        pdf.text(44, y-12, r[0], 10, (0.15,0.15,0.15))
        pdf.text(40+colw[0]+4, y-12, r[1], 10, (0,0,0))
        y -= 18
    y -= 16
    pdf.text(40, y, "2 Test Result Summary", 14, (0.1,0.1,0.1), bold=True)
    y -= 18
    header = ["Module Name", "Passed", "Failed", "Skipped", "Total", "Coverage"]
    name_w = cw * 0.40
    even_w = (cw - name_w) / 5.0
    colw2 = [name_w, even_w, even_w, even_w, even_w, even_w]
    rows2 = [header]
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    total_cases = 0
    sorted_mods = sorted(mods.values(), key=lambda d: (d.get("name") or ""))
    for v in sorted_mods:
        cov_str = "0%"
        if v["cases"]:
            cov_pct = (v["passed"] / v["cases"]) * 100.0
            cov_str = _fmt_pct(cov_pct)
        mname = v.get("name") or ""
        label = mname or ""
        rows2.append([label, str(v["passed"]), str(v["failed"]), str(v["skipped"]), str(v["cases"]), cov_str])
        total_passed += int(v["passed"])
        total_failed += int(v["failed"])
        total_skipped += int(v["skipped"])
        total_cases += int(v["cases"])
    total_cov_str = "0%"
    if total_cases:
        total_cov_pct = (total_passed / total_cases) * 100.0
        total_cov_str = _fmt_pct(total_cov_pct)
    rows2.append(["Total", str(total_passed), str(total_failed), str(total_skipped), str(total_cases), total_cov_str])
    y = _draw_table(pdf, 40, y, colw2, 18, rows2, header=True, zebra=True)
    y -= 16
    pdf.text(40, y, "3 Test Result", 14, (0.1,0.1,0.1), bold=True)
    y -= 18
    header3 = ["", "Test file", "Test Case", "Result", "Duration"]
    colw3 = [cw*0.07, cw*0.33, cw*0.38, cw*0.12, cw*0.10]
    rows3 = [header3] + case_rows
    y = _draw_table(pdf, 40, y, colw3, 18, rows3, header=True, zebra=True, result_col=3)
    if y < 120:
        pdf.new_page()
        y = h - 40
    y -= 16
    pdf.text(40, y, "4 Detail Result", 14, (0.1,0.1,0.1), bold=True)
    y -= 18
    groups: dict[str, list[dict]] = {}
    for d in details:
        s = (d.get("suite") or "").replace("\\", "/")
        if "/" in s:
            folder = os.path.basename(os.path.dirname(s))
        else:
            folder = "tests"
        groups.setdefault(folder, []).append(d)
    folder_idx = 1
    for folder, items in groups.items():
        if y < 100:
            pdf.new_page()
            y = h - 40
        pdf.text(40, y, f"4.{folder_idx} Test folder: {folder}", 12, (0.1,0.1,0.1), bold=True)
        y -= 16
        file_idx = 1
        for d in items:
            rows_needed = 6
            need_h = 16 + 22 + rows_needed*18 + 12
            if y - need_h < 100:
                pdf.new_page()
                y = h - 40
            file_name = os.path.basename((d.get("suite") or "").replace("\\", "/"))
            pdf.text(40, y, f"4.{folder_idx}.{file_idx} Test file: {file_name}", 12, (0.1,0.1,0.1), bold=True)
            y -= 16
            pdf.text(40, y, f"Test case: {d['case']}", 12, (0.1,0.1,0.1), bold=True)
            y -= 22
        colw = [150, cw - 150]
        grid = [["Status", d["status"]], ["Test file", d["suite"]], ["Test Case", d["case"]], ["Timestamps", summary["period"].split(" to ")[0]]]
        for r in grid:
            pdf.rect(40, y-18, sum(colw), 18, fill=False, stroke=True)
            lab_col = (0,0,0)
            val_col = (0,0,0)
            if r[0] == "Status":
                t = r[1].lower()
                if "passed" in t:
                    val_col = (0.2,0.6,0.2)
                elif "failed" in t:
                    val_col = (0.85,0.2,0.2)
                elif "skipped" in t:
                    val_col = (0.8,0.5,0.0)
                elif "error" in t:
                    val_col = (0.85,0.2,0.2)
            pdf.text(44, y-12, r[0], 10, lab_col, bold=True)
            pdf.text(40+colw[0]+4, y-12, r[1][:300], 10, val_col)
            y -= 18
        y -= 8
        pdf.rect(40, y-18, sum(colw), 18, fill=False, stroke=True)
        pdf.text(44, y-12, "Duration", 10, (0,0,0))
        pdf.text(40+colw[0]+4, y-12, d["duration"], 10, (0,0,0))
        y -= 18
        pdf.rect(40, y-18, sum(colw), 18, fill=False, stroke=True)
        pdf.text(44, y-12, "Screen Capture(s)", 10, (0,0,0))
        shots = [p for p in (d.get("screenshots", []) or []) if os.path.isfile(p)]
        sc_txt = ", ".join([os.path.basename(s) for s in shots[:4]])[:300] if shots else "No Screen Capture Provided"
        pdf.text(40+colw[0]+4, y-12, sc_txt, 9, (0,0,0))
        y -= 18
        t = d["status"].lower()
        if ("failed" in t or "error" in t) and d.get("error_message"):
            y -= 6
            pdf.text(40, y, "Error Message:", 10, (0,0,0), bold=True)
            y -= 14
            raw_lines = str(d.get("error_message") or "").splitlines()[:200]
            lines: list[str] = []
            max_chars = max(20, int((block_w - 16) / (9 * 0.53)))
            for ln in raw_lines:
                if len(ln) <= max_chars:
                    lines.append(ln)
                else:
                    parts = re.findall(r"\S+\s*", ln)
                    cur = ""
                    for tok in parts:
                        if len(cur) + len(tok) <= max_chars:
                            cur += tok
                        else:
                            if cur:
                                lines.append(cur.rstrip())
                            if len(tok) > max_chars:
                                i = 0
                                while i < len(tok):
                                    lines.append(tok[i:i+max_chars])
                                    i += max_chars
                                cur = ""
                            else:
                                cur = tok
                    lines.append(cur.rstrip())
            block_w = int(cw)
            x0 = 40
            block_h = 16 + 12*len(lines)
            pdf.set_fill_rgb(0.965,0.965,0.965)
            pdf.rect(x0, y - block_h, block_w, block_h, fill=True, stroke=False)
            pdf.set_stroke_rgb(0.75,0.75,0.75)
            pdf.rect(x0, y - block_h, block_w, block_h, fill=False, stroke=True)
            ty = y - 10
            for line in lines:
                text = line[:400]
                line_w = min(len(text), 400) * (9 * 0.53)
                tx = x0 + max(8, (block_w - line_w)/2)
                col = (0.85,0.2,0.2)
                pdf.text(int(tx), ty, text, 9, col)
                ty -= 12
            y -= block_h
            file_idx += 1
            y -= 12
            if y < 100:
                pdf.new_page()
                y = h - 40
        folder_idx += 1
    pdf.save(out_path)
    return out_path
def _wrap_error_text(text: str, max_width_pts: int, font_name: str = "Helvetica", font_size: int = 9) -> str:
    out_lines: list[str] = []
    for raw in (text or "").splitlines():
        indent_match = re.match(r"^[\t ]+", raw)
        indent = indent_match.group(0) if indent_match else ""
        rest = raw[len(indent):]
        cur = indent
        cur_w = stringWidth(cur, font_name, font_size)
        for tok in re.findall(r"\S+\s*", rest):
            tw = stringWidth(tok, font_name, font_size)
            if cur_w + tw <= max_width_pts:
                cur += tok
                cur_w += tw
            else:
                if cur:
                    out_lines.append(cur.rstrip())
                # token may be too long: hard cut
                if tw > max_width_pts:
                    buf = ""
                    bw = 0.0
                    for ch in tok:
                        cw = stringWidth(ch, font_name, font_size)
                        if bw + cw > max_width_pts:
                            out_lines.append((indent + buf).rstrip())
                            buf = ch
                            bw = cw
                        else:
                            buf += ch
                            bw += cw
                    cur = indent + buf
                    cur_w = stringWidth(cur, font_name, font_size)
                else:
                    cur = indent + tok
                    cur_w = stringWidth(cur, font_name, font_size)
        out_lines.append(cur.rstrip())
    return "\n".join(out_lines)

def _short_exc(msg: str) -> str:
    try:
        s = str(msg or "")
        i = s.find(":")
        return s if i < 0 else s[:i]
    except Exception:
        return ""

def _compose_anchor(t: dict, err_text: str = "") -> str:
    try:
        call = t.get("call") or {}
        lr = call.get("longrepr")
        path = None
        lineno = None
        message = ""
        if isinstance(lr, dict):
            rc = lr.get("reprcrash", {})
            path = rc.get("path")
            lineno = rc.get("lineno")
            message = rc.get("message", "")
        elif isinstance(lr, str):
            try:
                m = re.search(r"([\\/A-Za-z0-9_ .-]+\.py):(\d+):\s*([^\n]+)", lr)
                if m:
                    path = m.group(1)
                    lineno = int(m.group(2))
                    message = m.group(3)
            except Exception:
                pass
        if not path and err_text:
            try:
                m2 = re.search(r"([\\/A-Za-z0-9_ .-]+\.py):(\d+):\s*([^\n]+)", err_text)
                if m2:
                    path = m2.group(1)
                    lineno = int(m2.group(2))
                    message = m2.group(3)
            except Exception:
                pass
        if path:
            rp = os.path.relpath(path, PROJECT_ROOT) if os.path.isabs(path) else path
            exc = _short_exc(message)
            if lineno is not None:
                try:
                    ln = int(lineno)
                except Exception:
                    ln = lineno
                return f"{rp}:{ln}: {exc or message}".strip()
            return f"{rp}: {exc or message}".strip()
    except Exception:
        pass
    return ""

def _post_err(err_text: str, t: dict) -> str:
    s = err_text or ""
    try:
        m = re.search(r"Stacktrace", s, flags=re.IGNORECASE)
        if m:
            s = s[:m.start()].rstrip()
    except Exception:
        pass
    anchor = _compose_anchor(t, s)
    if anchor:
        s = (anchor + ("\n" if s else "") + s.rstrip())
    return s

def _html_unescape_multi(s: str) -> str:
    try:
        prev = None
        cur = s
        for _ in range(5):
            prev = cur
            cur = html.unescape(prev)
            if cur == prev:
                break
        return cur
    except Exception:
        return s

def _cleanup_err_text(s: str) -> str:
    try:
        s = _html_unescape_multi(s)
        s = s.replace("\r\n", "\n").replace("\r", "\n")
        lines = s.split("\n")
        out = []
        blank = False
        for ln in lines:
            t = ln.strip()
            if not t:
                if not blank:
                    out.append("")
                    blank = True
                continue
            if re.fullmatch(r"[\-=._~`─—┄┈]{4,}", t):
                continue
            out.append(ln)
            blank = False
        return "\n".join(out)
    except Exception:
        return s

def _fmt_pct(v: float) -> str:
    try:
        s = f"{v:.2f}"
        if s.endswith(".00"):
            s = str(int(round(v)))
        else:
            s = s.rstrip("0").rstrip(".")
        return s + "%"
    except Exception:
        return f"{v}%"
