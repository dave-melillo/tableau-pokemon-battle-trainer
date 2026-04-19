"""
Build a .twbx Tableau packaged workbook from a JSON config.

Config schema (see examples/pokemon_config.json):
{
  "title": "Pokemon Stats Explorer",
  "data_csv": "/abs/path/to/pokemon.csv",
  "output_twbx": "/abs/path/to/output.twbx",
  "datasource_caption": "pokemon",
  "columns": [                        # from inspect_data.py — ALL columns of the CSV
    {"name": "type1", "datatype": "string", "role": "dimension"},
    {"name": "attack", "datatype": "integer", "role": "measure"},
    ...
  ],
  "calculated_fields": [
    {"caption": "Total Stats", "datatype": "integer", "role": "measure",
     "type": "quantitative", "formula": "[hp]+[attack]+[defense]+[sp_attack]+[sp_defense]+[speed]"}
  ],
  "worksheets": [
    {
      "name": "Avg Total by Type",
      "mark": "Bar",                  # Automatic | Bar | Line | Circle | Square | Text | Map
      "rows": [{"field": "Total Stats", "agg": "Avg"}],
      "cols": [{"field": "type1", "agg": "None"}],
      "color": {"field": "is_legendary", "agg": "None"}    # optional
    }
  ],
  "dashboard": {
    "name": "Pokemon Dashboard",
    "size": [1200, 800],              # [width, height]
    "sheets": ["Avg Total by Type", "..."]   # listed top-to-bottom, stacked vertically
  }
}

Field references in worksheets use either the original column NAME (e.g. "type1") or
the calculated-field CAPTION (e.g. "Total Stats"). The script resolves them.
"""
from __future__ import annotations
import csv
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


def read_csv_headers(csv_path: Path) -> list[str]:
    """Return the full list of column headers from the CSV (not a subset)."""
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return next(reader)


def infer_csv_column_type(csv_path: Path, idx: int) -> str:
    """Sniff a column's type by scanning a sample of values."""
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        samples = []
        for i, row in enumerate(reader):
            if i >= 200:
                break
            if idx < len(row) and row[idx] != "":
                samples.append(row[idx])
    if not samples:
        return "string"
    int_ok = real_ok = date_ok = True
    for v in samples:
        if int_ok:
            try:
                int(v)
            except ValueError:
                int_ok = False
        if real_ok:
            try:
                float(v)
            except ValueError:
                real_ok = False
        if date_ok:
            if not (len(v) >= 8 and v[:4].isdigit() and ("-" in v or "/" in v)):
                date_ok = False
    if int_ok:
        return "integer"
    if real_ok:
        return "real"
    if date_ok:
        return "date"
    return "string"


AGG_PREFIX = {
    "None": "none", "Sum": "sum", "Avg": "avg", "Count": "cnt", "Countd": "ctd",
    "Min": "min", "Max": "max", "Year": "yr", "Quarter": "qr", "Month": "mn", "Day": "dy",
}
# Tableau XML enum values for <column-instance derivation='...'>. Some config names
# (user-facing) differ from the XML enum values — map them here.
DERIV_XML = {
    "None": "None", "Sum": "Sum", "Avg": "Avg", "Count": "Count", "Countd": "CountD",
    "Min": "Min", "Max": "Max", "Year": "Year", "Quarter": "Quarter", "Month": "Month", "Day": "Day",
}
# Allowed child elements of <encodings> per Tableau XML schema.
ALLOWED_ENCODINGS = {"color", "size", "shape", "text", "tooltip", "path", "level", "lod", "geometry"}
TYPE_KEY_SUFFIX = {"nominal": "nk", "ordinal": "ok", "quantitative": "qk"}


def hid(seed: str, length: int = 28) -> str:
    return hashlib.md5(seed.encode()).hexdigest()[:length]


def chash(seed: str) -> str:
    """32-char uppercase hash for object-id refs."""
    return hashlib.md5(seed.encode()).hexdigest().upper()[:32]


def role_to_type(role: str, datatype: str) -> str:
    if role == "measure":
        return "quantitative"
    if datatype in ("integer", "real", "date", "datetime"):
        return "ordinal"
    return "nominal"


def datatype_to_remote_type(dt: str) -> int:
    return {"integer": 20, "real": 5, "string": 130, "date": 7, "datetime": 7, "boolean": 11}.get(dt, 130)


def datatype_to_default_agg(dt: str, role: str) -> str:
    if role == "measure":
        return {"integer": "Sum", "real": "Sum"}.get(dt, "Count")
    return {"integer": "Sum", "real": "Sum", "date": "Year", "datetime": "Year"}.get(dt, "Count")


def esc(s: str) -> str:
    return xml_escape(s, {"'": "&apos;", '"': "&quot;"})


def encode_formula(formula: str) -> str:
    """Tableau encodes newlines as &#13;&#10; and escapes &/<>/quotes."""
    s = formula.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace('"', "&quot;").replace("'", "&apos;")
    s = s.replace("\r\n", "&#13;&#10;").replace("\n", "&#13;&#10;")
    return s


def build_workbook(cfg: dict) -> str:
    csv_path = Path(cfg["data_csv"]).resolve()
    csv_filename = csv_path.name
    csv_directory = str(csv_path.parent)
    table_name = csv_path.stem
    table_ref = f"[{table_name}#csv]"

    ds_caption = cfg.get("datasource_caption", table_name)
    seed = cfg.get("title", table_name)
    ds_name = f"federated.{hid(seed + ds_caption, 28)}"
    nc_name = f"textscan.{hid(seed + csv_filename, 28)}"
    parent_obj_id = f"[{csv_filename}_{chash(seed + csv_filename)}]"

    columns = cfg["columns"]
    calc_fields = cfg.get("calculated_fields", [])

    # Read the full CSV header list so the textscan connection metadata accurately
    # describes the source file. Without this, Tableau crashes when opening the
    # Data Source view because the <columns> block omits columns that exist in the CSV.
    all_csv_headers = read_csv_headers(csv_path)
    declared_types = {c["name"]: c["datatype"] for c in columns}
    full_columns_for_textscan = []
    for i, h in enumerate(all_csv_headers):
        dtype = declared_types.get(h) or infer_csv_column_type(csv_path, i)
        full_columns_for_textscan.append({"name": h, "datatype": dtype, "ordinal": i})

    # Map of caption -> calc_field info, including a generated internal name [Calculation_<id>]
    for i, cf in enumerate(calc_fields):
        cf["_name"] = f"[Calculation_{hid(cf['caption'] + str(i), 18)}]"
        cf["_role"] = cf.get("role", "measure")
        cf["_type"] = cf.get("type", role_to_type(cf["_role"], cf.get("datatype", "real")))

    # Resolve a field reference (used in worksheets) -> (column_name_in_brackets, datatype, role, is_calc)
    by_name = {c["name"]: c for c in columns}
    by_caption = {cf["caption"]: cf for cf in calc_fields}

    def resolve(field: str):
        if field in by_caption:
            cf = by_caption[field]
            return cf["_name"], cf["datatype"], cf["_role"], True
        if field in by_name:
            c = by_name[field]
            return f"[{c['name']}]", c["datatype"], c.get("role", "dimension"), False
        raise ValueError(f"Field not found in columns or calculated_fields: {field}")

    # ---- Header / manifest ----
    out = [
        "<?xml version='1.0' encoding='utf-8' ?>",
        "",
        "<!-- generated by tableau-workbook skill -->",
        "<workbook original-version='18.1' source-build='2021.4.3 (20214.22.0108.1039)' "
        "source-platform='mac' version='18.1' "
        "xmlns:user='http://www.tableausoftware.com/xml/user'>",
        "  <document-format-change-manifest>",
        "    <_.fcp.AnimationOnByDefault.true...AnimationOnByDefault />",
        "    <_.fcp.MarkAnimation.true...MarkAnimation />",
        "    <_.fcp.ObjectModelEncapsulateLegacy.true...ObjectModelEncapsulateLegacy />",
        "    <_.fcp.ObjectModelExtractV2.true...ObjectModelExtractV2 />",
        "    <_.fcp.ObjectModelTableType.true...ObjectModelTableType />",
        "    <_.fcp.SchemaViewerObjectModel.true...SchemaViewerObjectModel />",
        "    <SheetIdentifierTracking />",
        "    <WindowsPersistSimpleIdentifiers />",
        "  </document-format-change-manifest>",
        "  <preferences>",
        "    <preference name='ui.encoding.shelf.height' value='24' />",
        "    <preference name='ui.shelf.height' value='26' />",
        "  </preferences>",
        "  <datasources>",
    ]

    # ---- Datasource ----
    out += [
        f"    <datasource caption='{esc(ds_caption)}' inline='true' name='{ds_name}' version='18.1'>",
        "      <connection class='federated'>",
        "        <named-connections>",
        f"          <named-connection caption='{esc(ds_caption)}' name='{nc_name}'>",
        # Absolute source directory; Tableau falls back to bundled Data/ if not found.
        f"            <connection class='textscan' directory='{esc(csv_directory)}' workgroup-auth-mode='as-is' />",
        "          </named-connection>",
        "        </named-connections>",
    ]
    # Two relation blocks (legacy + encapsulated) for version safety
    for ns_prefix in (
        "_.fcp.ObjectModelEncapsulateLegacy.false...",
        "_.fcp.ObjectModelEncapsulateLegacy.true...",
    ):
        out += [
            f"        <{ns_prefix}relation connection='{nc_name}' name='{csv_filename}' table='{table_ref}' type='table'>",
            "          <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>",
        ]
        for c in full_columns_for_textscan:
            out.append(f"            <column datatype='{c['datatype']}' name='{esc(c['name'])}' ordinal='{c['ordinal']}' />")
        out += [
            "          </columns>",
            f"        </{ns_prefix}relation>",
        ]
    # Metadata records (capability + per-column)
    out += [
        "        <metadata-records>",
        "          <metadata-record class='capability'>",
        "            <remote-name />",
        "            <remote-type>0</remote-type>",
        f"            <parent-name>[{csv_filename}]</parent-name>",
        "            <remote-alias />",
        "            <aggregation>Count</aggregation>",
        "            <contains-null>true</contains-null>",
        "            <attributes>",
        "              <attribute datatype='string' name='character-set'>&quot;UTF-8&quot;</attribute>",
        "              <attribute datatype='string' name='collation'>&quot;en_US&quot;</attribute>",
        "              <attribute datatype='string' name='field-delimiter'>&quot;,&quot;</attribute>",
        "              <attribute datatype='string' name='header-row'>&quot;true&quot;</attribute>",
        "              <attribute datatype='string' name='locale'>&quot;en_US&quot;</attribute>",
        "              <attribute datatype='string' name='single-char'>&quot;&quot;</attribute>",
        "            </attributes>",
        "          </metadata-record>",
    ]
    # Emit a metadata-record for EVERY CSV column (not just declared), so the
    # source connection accurately describes the underlying file.
    for c in full_columns_for_textscan:
        agg = datatype_to_default_agg(c["datatype"], "dimension" if c["datatype"] in ("string", "date") else "measure")
        out += [
            "          <metadata-record class='column'>",
            f"            <remote-name>{esc(c['name'])}</remote-name>",
            f"            <remote-type>{datatype_to_remote_type(c['datatype'])}</remote-type>",
            f"            <local-name>[{esc(c['name'])}]</local-name>",
            f"            <parent-name>[{csv_filename}]</parent-name>",
            f"            <remote-alias>{esc(c['name'])}</remote-alias>",
            f"            <ordinal>{c['ordinal']}</ordinal>",
            f"            <local-type>{c['datatype']}</local-type>",
            f"            <aggregation>{agg}</aggregation>",
            "            <contains-null>true</contains-null>",
            f"            <_.fcp.ObjectModelEncapsulateLegacy.true...object-id>{parent_obj_id}</_.fcp.ObjectModelEncapsulateLegacy.true...object-id>",
            "          </metadata-record>",
        ]
    out += [
        "        </metadata-records>",
        "      </connection>",
        "      <aliases enabled='yes' />",
    ]
    # Calculated field column declarations
    for cf in calc_fields:
        out += [
            f"      <column caption='{esc(cf['caption'])}' datatype='{cf['datatype']}' "
            f"name='{cf['_name']}' role='{cf['_role']}' type='{cf['_type']}'>",
            f"        <calculation class='tableau' formula='{encode_formula(cf['formula'])}' />",
            "      </column>",
        ]
    # Regular column declarations (use friendly captions = original names)
    for c in columns:
        rtype = role_to_type(c.get("role", "dimension"), c["datatype"])
        sem = f" semantic-role='{esc(c['semantic_role'])}'" if c.get("semantic_role") else ""
        out.append(
            f"      <column caption='{esc(c['name'])}' datatype='{c['datatype']}' "
            f"name='[{esc(c['name'])}]' role='{c.get('role', 'dimension')}'{sem} type='{rtype}' />"
        )
    # ---- Extract block (Tableau Public requires this; Desktop tolerates it) ----
    hyper_rel = f"Data/{table_name}.hyper"
    out += [
        f"      <extract _.fcp.ObjectModelExtractV2.true...object-id='' count='-1' enabled='true' units='records'>",
        f"        <connection access_mode='readonly' author-locale='en_US' class='hyper' "
        f"dbname='{hyper_rel}' default-settings='hyper' schema='Extract' sslmode='' "
        f"tablename='Extract' update-time='01/01/2026 12:00:00 AM' username='tableau_internal_user'>",
        "          <_.fcp.ObjectModelEncapsulateLegacy.false...relation name='Extract' table='[Extract].[Extract]' type='table' />",
        "          <_.fcp.ObjectModelEncapsulateLegacy.true...relation name='Extract' table='[Extract].[Extract]' type='table' />",
        "          <metadata-records>",
    ]
    # Extract date columns get remote-type 133 (date in extract); strings 129
    extract_remote_type = {"integer": 20, "real": 5, "string": 129, "date": 133, "datetime": 133, "boolean": 11}
    for i, c in enumerate(columns):
        agg = datatype_to_default_agg(c["datatype"], c.get("role", "dimension"))
        out += [
            "            <metadata-record class='column'>",
            f"              <remote-name>{esc(c['name'])}</remote-name>",
            f"              <remote-type>{extract_remote_type.get(c['datatype'], 129)}</remote-type>",
            f"              <local-name>[{esc(c['name'])}]</local-name>",
            "              <parent-name>[Extract]</parent-name>",
            f"              <remote-alias>{esc(c['name'])}</remote-alias>",
            f"              <ordinal>{i}</ordinal>",
            f"              <family>{esc(table_name)}</family>",
            f"              <local-type>{c['datatype']}</local-type>",
            f"              <aggregation>{agg}</aggregation>",
            "              <contains-null>true</contains-null>",
            f"              <_.fcp.ObjectModelEncapsulateLegacy.true...object-id>{parent_obj_id}</_.fcp.ObjectModelEncapsulateLegacy.true...object-id>",
            "            </metadata-record>",
        ]
    out += [
        "          </metadata-records>",
        "        </connection>",
        "      </extract>",
    ]
    # Object graph: the new Object Model representation. Without this, the Data Source
    # view crashes because Tableau 2020.2+ uses this as the schema viewer data.
    out += [
        "      <layout dim-ordering='alphabetic' measure-ordering='alphabetic' show-structure='true' />",
        "      <_.fcp.ObjectModelEncapsulateLegacy.true...object-graph>",
        "        <objects>",
        f"          <object caption='{esc(csv_filename)}' id='{parent_obj_id[1:-1]}'>",
        "            <properties context=''>",
        f"              <relation connection='{nc_name}' name='{esc(csv_filename)}' table='{table_ref}' type='table'>",
        "                <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>",
    ]
    for c in full_columns_for_textscan:
        out.append(
            f"                  <column datatype='{c['datatype']}' name='{esc(c['name'])}' ordinal='{c['ordinal']}' />"
        )
    out += [
        "                </columns>",
        "              </relation>",
        "            </properties>",
        "            <properties context='extract'>",
        "              <relation name='Extract' table='[Extract].[Extract]' type='table' />",
        "            </properties>",
        "          </object>",
        "        </objects>",
        "      </_.fcp.ObjectModelEncapsulateLegacy.true...object-graph>",
        "    </datasource>",
        "  </datasources>",
    ]

    # ---- Worksheets ----
    worksheets = cfg.get("worksheets", [])
    out.append("  <worksheets>")
    for ws in worksheets:
        out += build_worksheet(ws, ds_name, resolve)
    out.append("  </worksheets>")

    # ---- Dashboard ----
    dashboard = cfg.get("dashboard")
    if dashboard:
        out += build_dashboard(dashboard)

    # ---- Windows (one per worksheet + dashboard) ----
    out.append("  <windows source-height='30'>")
    for ws in worksheets:
        out += [
            f"    <window class='worksheet' name='{esc(ws['name'])}'>",
            "      <cards>",
            "        <edge name='left'>",
            "          <strip size='160'>",
            "            <card type='pages' />",
            "            <card type='filters' />",
            "            <card type='marks' />",
            "          </strip>",
            "        </edge>",
            "        <edge name='top'>",
            "          <strip size='2147483647'>",
            "            <card type='columns' />",
            "          </strip>",
            "          <strip size='2147483647'>",
            "            <card type='rows' />",
            "          </strip>",
            "          <strip size='31'>",
            "            <card type='title' />",
            "          </strip>",
            "        </edge>",
            "      </cards>",
            "      <viewpoint />",
            f"      <simple-id uuid='{{{hid(ws['name'] + 'win', 8).upper()}-{hid(ws['name'] + 'a', 4).upper()}-{hid(ws['name'] + 'b', 4).upper()}-{hid(ws['name'] + 'c', 4).upper()}-{hid(ws['name'] + 'd', 12).upper()}}}' />",
            "    </window>",
        ]
    if dashboard:
        out += [
            f"    <window class='dashboard' name='{esc(dashboard['name'])}'>",
            "      <viewpoints>",
        ]
        for sheet in dashboard["sheets"]:
            out.append(f"        <viewpoint name='{esc(sheet)}' />")
        out += [
            "      </viewpoints>",
            "      <active id='-1' />",
            "    </window>",
        ]
    out.append("  </windows>")
    out.append("</workbook>")
    return "\n".join(out)


def build_worksheet(ws: dict, ds_name: str, resolve) -> list[str]:
    name = ws["name"]
    mark = ws.get("mark", "Automatic")

    # Collect all field refs used in rows/cols/encodings
    shelves = {"rows": ws.get("rows", []), "cols": ws.get("cols", [])}
    encodings = {}
    for enc in ("color", "size", "shape", "label", "detail", "tooltip"):
        if enc in ws:
            encodings[enc] = ws[enc] if isinstance(ws[enc], list) else [ws[enc]]

    # Build column-instance entries: dedupe by (col_internal_name, agg)
    declared_cols = {}    # col_internal_name -> (datatype, role, is_calc)
    instances = {}        # (col_internal_name, agg) -> instance_local_name

    def register(field: str, agg: str):
        col_name, dtype, role, is_calc = resolve(field)
        declared_cols[col_name] = (dtype, role, is_calc, field)
        # column-instance naming: [<aggprefix>:<inner>:<keysuffix>]
        inner = col_name.strip("[]")
        prefix = AGG_PREFIX.get(agg, "none")
        # Aggregating (Sum/Avg/Count/Countd/Min/Max) always yields quantitative.
        if agg in ("Sum", "Avg", "Count", "Countd", "Min", "Max"):
            kind = "quantitative"
        else:
            kind = role_to_type(role, dtype)
        suffix = TYPE_KEY_SUFFIX[kind]
        inst_name = f"[{prefix}:{inner}:{suffix}]"
        instances[(col_name, agg)] = (inst_name, kind)
        return inst_name, kind

    for shelf_fields in shelves.values():
        for f in shelf_fields:
            register(f["field"], f.get("agg", "None"))
    for enc_list in encodings.values():
        for f in enc_list:
            register(f["field"], f.get("agg", "None"))

    out = [f"    <worksheet name='{esc(name)}'>"]
    out += [
        "      <table>",
        "        <view>",
        "          <datasources>",
        f"            <datasource caption='{esc(name)}-ds' name='{ds_name}' />",
        "          </datasources>",
        f"          <datasource-dependencies datasource='{ds_name}'>",
    ]
    # Declare each unique column used
    for col_name, (dtype, role, is_calc, friendly) in declared_cols.items():
        rtype = role_to_type(role, dtype)
        out.append(
            f"            <column caption='{esc(friendly)}' datatype='{dtype}' "
            f"name='{col_name}' role='{role}' type='{rtype}' />"
        )
    # Declare each unique column-instance
    for (col_name, agg), (inst_name, kind) in instances.items():
        deriv = DERIV_XML.get(agg, "None")
        out.append(
            f"            <column-instance column='{col_name}' derivation='{deriv}' "
            f"name='{inst_name}' pivot='key' type='{kind}' />"
        )
    out += [
        "          </datasource-dependencies>",
        "          <aggregation value='true' />",
        "        </view>",
        "        <style />",
        "        <panes>",
        "          <pane selection-relaxation-option='selection-relaxation-allow'>",
        "            <view>",
        "              <breakdown value='auto' />",
        "            </view>",
    ]
    # Mark class: 'Map' isn't a valid XML enum value. Geographic viz uses
    # 'Automatic' (auto-renders as map once lat/lon are on shelves with
    # Latitude/Longitude semantic roles).
    mark_xml = "Automatic" if mark == "Map" else mark
    out.append(f"            <mark class='{mark_xml}' />")
    # Filter encodings to schema-allowed elements. 'detail' and 'label' aren't
    # valid <encodings> children — caller should use dedicated shelves / tooltips.
    if encodings:
        valid = {k: v for k, v in encodings.items() if k in ALLOWED_ENCODINGS}
        if valid:
            out.append("            <encodings>")
            for enc_kind, enc_list in valid.items():
                for f in enc_list:
                    col_name, dtype, role, _ = resolve(f["field"])
                    inst_name, _ = instances[(col_name, f.get("agg", "None"))]
                    out.append(
                        f"              <{enc_kind} column='[{ds_name}].{inst_name}' />"
                    )
            out.append("            </encodings>")
    out += [
        "          </pane>",
        "        </panes>",
    ]

    def shelf_xml(fields: list[dict]) -> str:
        if not fields:
            return ""
        parts = []
        for f in fields:
            col_name, _, _, _ = resolve(f["field"])
            inst_name, _ = instances[(col_name, f.get("agg", "None"))]
            parts.append(f"[{ds_name}].{inst_name}")
        if len(parts) == 1:
            return parts[0]
        return "(" + " / ".join(parts) + ")"

    out.append(f"        <rows>{shelf_xml(shelves['rows'])}</rows>")
    out.append(f"        <cols>{shelf_xml(shelves['cols'])}</cols>")
    out += [
        "      </table>",
        f"      <simple-id uuid='{{{hid(name + 'ws', 8).upper()}-{hid(name + 'a', 4).upper()}-{hid(name + 'b', 4).upper()}-{hid(name + 'c', 4).upper()}-{hid(name + 'd', 12).upper()}}}' />",
        "    </worksheet>",
    ]
    return out


def build_dashboard(d: dict) -> list[str]:
    name = d["name"]
    width, height = d.get("size", [1200, 800])
    sheets = d["sheets"]
    n = len(sheets)
    out = [
        "  <dashboards>",
        f"    <dashboard name='{esc(name)}'>",
        "      <style />",
        f"      <size maxheight='{height}' maxwidth='{width}' minheight='{height}' minwidth='{width}' />",
        "      <zones>",
        "        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>",
        "          <zone h='100000' id='2' param='vert' type-v2='layout-flow' w='100000' x='0' y='0'>",
    ]
    # Stack each sheet vertically. Coordinates are 0-100000 scale.
    slot_h = 100000 // max(n, 1)
    for i, sheet in enumerate(sheets):
        out.append(
            f"            <zone h='{slot_h}' id='{10 + i}' name='{esc(sheet)}' "
            f"w='100000' x='0' y='{slot_h * i}' />"
        )
    out += [
        "          </zone>",
        "          <zone-style>",
        "            <format attr='border-color' value='#000000' />",
        "            <format attr='border-style' value='none' />",
        "            <format attr='border-width' value='0' />",
        "            <format attr='margin' value='8' />",
        "          </zone-style>",
        "        </zone>",
        "      </zones>",
        f"      <simple-id uuid='{{{hid(name + 'd', 8).upper()}-{hid(name + 'da', 4).upper()}-{hid(name + 'db', 4).upper()}-{hid(name + 'dc', 4).upper()}-{hid(name + 'dd', 12).upper()}}}' />",
        "    </dashboard>",
        "  </dashboards>",
    ]
    return out


def package_twbx(twb_xml: str, csv_path: Path, hyper_path: Path, output_twbx: Path) -> None:
    output_twbx.parent.mkdir(parents=True, exist_ok=True)
    table_name = csv_path.stem
    with zipfile.ZipFile(output_twbx, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{output_twbx.stem}.twb", twb_xml)
        zf.write(hyper_path, f"Data/{table_name}.hyper")
        # Bundle the CSV too as a backup source for editing in Desktop
        zf.write(csv_path, f"Data/{csv_path.name}")


def build_workbook_multi(cfg: dict, joined_columns: list[dict]) -> str:
    """Multi-table variant: declares multiple textscan named-connections joined via
    Tableau's <relation join='inner'> nested syntax. Used for joining lessons.
    Worksheets reference fields by their post-join name (with table-alias prefix)."""
    output_twbx = Path(cfg["output_twbx"])
    tables = cfg["tables"]
    joins_cfg = cfg["joins"]

    ds_caption = cfg.get("datasource_caption", "joined")
    seed = cfg.get("title", ds_caption)
    ds_name = f"federated.{hid(seed + ds_caption, 28)}"

    # Per-table metadata
    nc_names = {}            # alias -> textscan named-connection name
    csv_paths = {}           # alias -> Path
    csv_filenames = {}       # alias -> filename
    csv_dirs = {}            # alias -> dir
    csv_table_refs = {}      # alias -> [stem#csv]
    full_headers = {}        # alias -> [{name, datatype, ordinal}, ...]
    declared_columns = {}    # alias -> user-listed columns
    for t in tables:
        alias = t["alias"]
        path = Path(t["csv_path"]).resolve()
        csv_paths[alias] = path
        csv_filenames[alias] = path.name
        csv_dirs[alias] = str(path.parent)
        csv_table_refs[alias] = f"[{path.stem}#csv]"
        nc_names[alias] = f"textscan.{hid(seed + alias, 28)}"
        all_headers = read_csv_headers(path)
        declared_types = {c["name"]: c["datatype"] for c in t["columns"]}
        full_headers[alias] = [
            {"name": h, "datatype": declared_types.get(h) or infer_csv_column_type(path, i), "ordinal": i}
            for i, h in enumerate(all_headers)
        ]
        declared_columns[alias] = t["columns"]
    # ONE object-id for the entire joined logical object (matches the EasyJoins
    # template convention: all metadata records reference this single id).
    primary_alias = tables[0]["alias"]
    joined_obj_id = f"[{primary_alias}_{chash(seed)}]"

    calc_fields = cfg.get("calculated_fields", [])
    for i, cf in enumerate(calc_fields):
        cf["_name"] = f"[Calculation_{hid(cf['caption'] + str(i), 18)}]"
        cf["_role"] = cf.get("role", "measure")
        cf["_type"] = cf.get("type", role_to_type(cf["_role"], cf.get("datatype", "real")))

    # Resolve a field reference. For multi-table, the field is the joined column name
    # (post-prefix). joined_columns lists every available extract column.
    by_extract_name = {c["name"]: c for c in joined_columns}
    by_caption = {cf["caption"]: cf for cf in calc_fields}

    def resolve(field: str):
        if field in by_caption:
            cf = by_caption[field]
            return cf["_name"], cf["datatype"], cf["_role"], True
        if field in by_extract_name:
            c = by_extract_name[field]
            return f"[{field}]", c["datatype"], c.get("role", "dimension"), False
        raise ValueError(f"Field {field!r} not found in joined columns or calc fields. "
                         f"Available: {list(by_extract_name)[:10]}...")

    # Build relation tree string (left-deep). Internally all relations use plain
    # <relation> tags; only the OUTERMOST gets the FCP namespace prefix when
    # emitted (matching how Tableau Desktop writes joined workbooks).
    single = {}
    for alias, headers in full_headers.items():
        ll = []
        ll.append(f"          <relation connection='{nc_names[alias]}' name='{esc(alias)}' table='{csv_table_refs[alias]}' type='table'>")
        ll.append(f"            <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>")
        for c in headers:
            ll.append(f"              <column datatype='{c['datatype']}' name='{esc(c['name'])}' ordinal='{c['ordinal']}' />")
        ll.append(f"            </columns>")
        ll.append(f"          </relation>")
        single[alias] = ll

    def build_inner_tree() -> list[str]:
        """Plain <relation> tree (no namespace prefix)."""
        if not joins_cfg:
            return single[list(full_headers)[0]]
        first = joins_cfg[0]
        out = [
            f"        <relation join='{first.get('join_type', 'inner')}' type='join'>",
            f"          <clause type='join'>",
            f"            <expression op='='>",
            f"              <expression op='[{first['left_table']}].[{first['left_col']}]' />",
            f"              <expression op='[{first['right_table']}].[{first['right_col']}]' />",
            f"            </expression>",
            f"          </clause>",
        ]
        out += [f"  {l}" for l in single[first["left_table"]]]
        out += [f"  {l}" for l in single[first["right_table"]]]
        out.append(f"        </relation>")
        for j in joins_cfg[1:]:
            inner = out
            out = [
                f"        <relation join='{j.get('join_type', 'inner')}' type='join'>",
                f"          <clause type='join'>",
                f"            <expression op='='>",
                f"              <expression op='[{j['left_table']}].[{j['left_col']}]' />",
                f"              <expression op='[{j['right_table']}].[{j['right_col']}]' />",
                f"            </expression>",
                f"          </clause>",
            ]
            out += ["  " + l for l in inner]
            out += [f"  {l}" for l in single[j["right_table"]]]
            out.append(f"        </relation>")
        return out

    def build_relation_tree(ns_prefix: str) -> list[str]:
        inner = build_inner_tree()
        # Wrap outermost open/close with the FCP namespace prefix
        if not inner:
            return inner
        first_line = inner[0].replace("<relation", f"<{ns_prefix}relation", 1)
        last_line = inner[-1].replace("</relation>", f"</{ns_prefix}relation>", 1)
        return [first_line] + inner[1:-1] + [last_line]

    # ---- Header / manifest ----
    out = [
        "<?xml version='1.0' encoding='utf-8' ?>",
        "",
        "<!-- generated by tableau-workbook skill (multi-table) -->",
        "<workbook original-version='18.1' source-build='2021.4.3 (20214.22.0108.1039)' "
        "source-platform='mac' version='18.1' "
        "xmlns:user='http://www.tableausoftware.com/xml/user'>",
        "  <document-format-change-manifest>",
        "    <_.fcp.AnimationOnByDefault.true...AnimationOnByDefault />",
        "    <_.fcp.MarkAnimation.true...MarkAnimation />",
        "    <_.fcp.ObjectModelEncapsulateLegacy.true...ObjectModelEncapsulateLegacy />",
        "    <_.fcp.ObjectModelExtractV2.true...ObjectModelExtractV2 />",
        "    <_.fcp.ObjectModelTableType.true...ObjectModelTableType />",
        "    <_.fcp.SchemaViewerObjectModel.true...SchemaViewerObjectModel />",
        "    <SheetIdentifierTracking />",
        "    <WindowsPersistSimpleIdentifiers />",
        "  </document-format-change-manifest>",
        "  <preferences>",
        "    <preference name='ui.encoding.shelf.height' value='24' />",
        "    <preference name='ui.shelf.height' value='26' />",
        "  </preferences>",
        "  <datasources>",
    ]

    out.append(f"    <datasource caption='{esc(ds_caption)}' inline='true' name='{ds_name}' version='18.1'>")
    out.append("      <connection class='federated'>")
    out.append("        <named-connections>")
    for alias in full_headers:
        out.append(f"          <named-connection caption='{esc(alias)}' name='{nc_names[alias]}'>")
        out.append(f"            <connection class='textscan' directory='{esc(csv_dirs[alias])}' filename='{esc(csv_filenames[alias])}' workgroup-auth-mode='as-is' />")
        out.append(f"          </named-connection>")
    out.append("        </named-connections>")
    # Two relation trees: legacy and encapsulated
    for ns_prefix in (
        "_.fcp.ObjectModelEncapsulateLegacy.false...",
        "_.fcp.ObjectModelEncapsulateLegacy.true...",
    ):
        out += build_relation_tree(ns_prefix)
    # Metadata records: ALL columns from ALL CSVs, plus a 'capability' record per table
    out.append("        <metadata-records>")
    for alias, headers in full_headers.items():
        out += [
            "          <metadata-record class='capability'>",
            "            <remote-name />",
            "            <remote-type>0</remote-type>",
            f"            <parent-name>[{esc(csv_filenames[alias])}]</parent-name>",
            "            <remote-alias />",
            "            <aggregation>Count</aggregation>",
            "            <contains-null>true</contains-null>",
            "            <attributes>",
            "              <attribute datatype='string' name='character-set'>&quot;UTF-8&quot;</attribute>",
            "              <attribute datatype='string' name='collation'>&quot;en_US&quot;</attribute>",
            "              <attribute datatype='string' name='field-delimiter'>&quot;,&quot;</attribute>",
            "              <attribute datatype='string' name='header-row'>&quot;true&quot;</attribute>",
            "              <attribute datatype='string' name='locale'>&quot;en_US&quot;</attribute>",
            "              <attribute datatype='string' name='single-char'>&quot;&quot;</attribute>",
            "            </attributes>",
            "          </metadata-record>",
        ]
        for c in headers:
            agg = datatype_to_default_agg(c["datatype"], "dimension" if c["datatype"] in ("string", "date") else "measure")
            out += [
                "          <metadata-record class='column'>",
                f"            <remote-name>{esc(c['name'])}</remote-name>",
                f"            <remote-type>{datatype_to_remote_type(c['datatype'])}</remote-type>",
                f"            <local-name>[{esc(c['name'])}]</local-name>",
                f"            <parent-name>[{esc(csv_filenames[alias])}]</parent-name>",
                f"            <remote-alias>{esc(c['name'])}</remote-alias>",
                f"            <ordinal>{c['ordinal']}</ordinal>",
                f"            <local-type>{c['datatype']}</local-type>",
                f"            <aggregation>{agg}</aggregation>",
                "            <contains-null>true</contains-null>",
                f"            <_.fcp.ObjectModelEncapsulateLegacy.true...object-id>{joined_obj_id}</_.fcp.ObjectModelEncapsulateLegacy.true...object-id>",
                "          </metadata-record>",
            ]
    out.append("        </metadata-records>")
    out.append("      </connection>")
    out.append("      <aliases enabled='yes' />")
    # Calc field column declarations
    for cf in calc_fields:
        out += [
            f"      <column caption='{esc(cf['caption'])}' datatype='{cf['datatype']}' "
            f"name='{cf['_name']}' role='{cf['_role']}' type='{cf['_type']}'>",
            f"        <calculation class='tableau' formula='{encode_formula(cf['formula'])}' />",
            "      </column>",
        ]
    # Column declarations: one per joined-extract column (using post-prefix names).
    # User-friendly captions come from the joined_columns 'caption' field if provided.
    for c in joined_columns:
        rtype = role_to_type(c.get("role", "dimension"), c["datatype"])
        sem = f" semantic-role='{esc(c['semantic_role'])}'" if c.get("semantic_role") else ""
        caption = c.get("caption", c["name"])
        out.append(
            f"      <column caption='{esc(caption)}' datatype='{c['datatype']}' "
            f"name='[{esc(c['name'])}]' role='{c.get('role', 'dimension')}'{sem} type='{rtype}' />"
        )
    # Extract block (cached joined data). All extract metadata records also
    # reference the same single joined_obj_id.
    hyper_rel = f"Data/{primary_alias}_joined.hyper"
    out += [
        f"      <extract _.fcp.ObjectModelExtractV2.true...object-id='' count='-1' enabled='true' units='records'>",
        f"        <connection access_mode='readonly' author-locale='en_US' class='hyper' "
        f"dbname='{hyper_rel}' default-settings='hyper' schema='Extract' sslmode='' "
        f"tablename='Extract' update-time='01/01/2026 12:00:00 AM' username='tableau_internal_user'>",
        "          <_.fcp.ObjectModelEncapsulateLegacy.false...relation name='Extract' table='[Extract].[Extract]' type='table' />",
        "          <_.fcp.ObjectModelEncapsulateLegacy.true...relation name='Extract' table='[Extract].[Extract]' type='table' />",
        "          <metadata-records>",
    ]
    extract_remote_type = {"integer": 20, "real": 5, "string": 129, "date": 133, "datetime": 133, "boolean": 11}
    for i, c in enumerate(joined_columns):
        agg = datatype_to_default_agg(c["datatype"], c.get("role", "dimension"))
        out += [
            "            <metadata-record class='column'>",
            f"              <remote-name>{esc(c['name'])}</remote-name>",
            f"              <remote-type>{extract_remote_type.get(c['datatype'], 129)}</remote-type>",
            f"              <local-name>[{esc(c['name'])}]</local-name>",
            "              <parent-name>[Extract]</parent-name>",
            f"              <remote-alias>{esc(c['name'])}</remote-alias>",
            f"              <ordinal>{i}</ordinal>",
            f"              <family>{esc(primary_alias)}</family>",
            f"              <local-type>{c['datatype']}</local-type>",
            f"              <aggregation>{agg}</aggregation>",
            "              <contains-null>true</contains-null>",
            f"              <_.fcp.ObjectModelEncapsulateLegacy.true...object-id>{joined_obj_id}</_.fcp.ObjectModelEncapsulateLegacy.true...object-id>",
            "            </metadata-record>",
        ]
    out += [
        "          </metadata-records>",
        "        </connection>",
        "      </extract>",
        "      <layout dim-ordering='alphabetic' measure-ordering='alphabetic' show-structure='true' />",
        # Object-graph: ONE object representing the joined logical entity, with
        # the full join tree embedded as its 'context=""' properties. Pattern
        # matches the instructor's EasyJoins template: single object, plain
        # nested <relation> tags inside, separate context='extract' properties.
        "      <_.fcp.ObjectModelEncapsulateLegacy.true...object-graph>",
        "        <objects>",
        f"          <object caption='{esc(primary_alias)}' id='{joined_obj_id[1:-1]}'>",
        "            <properties context=''>",
    ]
    # Embed the inner relation tree (plain tags) inside the object's properties
    inner_tree_for_obj = build_inner_tree()
    out += [f"      {l}" for l in inner_tree_for_obj]
    out += [
        "            </properties>",
        "            <properties context='extract'>",
        "              <relation name='Extract' table='[Extract].[Extract]' type='table' />",
        "            </properties>",
        "          </object>",
        "        </objects>",
        "      </_.fcp.ObjectModelEncapsulateLegacy.true...object-graph>",
        "    </datasource>",
        "  </datasources>",
    ]

    # Worksheets
    worksheets = cfg.get("worksheets", [])
    out.append("  <worksheets>")
    for ws in worksheets:
        out += build_worksheet(ws, ds_name, resolve)
    out.append("  </worksheets>")
    # Dashboard
    dashboard = cfg.get("dashboard")
    if dashboard:
        out += build_dashboard(dashboard)
    # Windows
    out.append("  <windows source-height='30'>")
    for ws in worksheets:
        out += [
            f"    <window class='worksheet' name='{esc(ws['name'])}'>",
            "      <cards>",
            "        <edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge>",
            "        <edge name='top'>",
            "          <strip size='2147483647'><card type='columns' /></strip>",
            "          <strip size='2147483647'><card type='rows' /></strip>",
            "          <strip size='31'><card type='title' /></strip>",
            "        </edge>",
            "      </cards>",
            "      <viewpoint />",
            f"      <simple-id uuid='{{{hid(ws['name'] + 'win', 8).upper()}-{hid(ws['name'] + 'a', 4).upper()}-{hid(ws['name'] + 'b', 4).upper()}-{hid(ws['name'] + 'c', 4).upper()}-{hid(ws['name'] + 'd', 12).upper()}}}' />",
            "    </window>",
        ]
    if dashboard:
        out += [
            f"    <window class='dashboard' name='{esc(dashboard['name'])}'>",
            "      <viewpoints>",
        ]
        for sheet in dashboard["sheets"]:
            out.append(f"        <viewpoint name='{esc(sheet)}' />")
        out += ["      </viewpoints>", "      <active id='-1' />", "    </window>"]
    out.append("  </windows>")
    out.append("</workbook>")
    return "\n".join(out)


def build_joined_dataframe_and_columns(cfg: dict):
    """Pandas-merge the configured tables. Returns (joined_df, joined_columns).
    Right-side non-key columns are prefixed with the right table alias."""
    import pandas as pd
    tables = cfg["tables"]
    joins_cfg = cfg["joins"]
    # Load each table into a dict by alias
    dfs = {t["alias"]: pd.read_csv(t["csv_path"]) for t in tables}
    # Track which columns end up in the joined df, with metadata
    joined_cols = []
    primary_alias = tables[0]["alias"]
    # Add primary-table columns first
    for c in tables[0]["columns"]:
        joined_cols.append({**c, "name": c["name"]})
    # Merge in the other tables. Track which tables are non-primary so we know
    # their columns are prefixed.
    df = dfs[primary_alias].copy()
    joined_aliases = {primary_alias}

    def actual_left_col(left_table: str, left_col: str) -> str:
        """Return the column name as it actually exists in the merged df."""
        if left_table == primary_alias:
            return left_col
        prefixed = f"{left_table}_{left_col}"
        return prefixed if prefixed in df.columns else left_col

    for j in joins_cfg:
        right_alias = j["right_table"]
        right_df = dfs[right_alias].copy()
        right_key = j["right_col"]
        rename_map = {c: f"{right_alias}_{c}" for c in right_df.columns if c != right_key}
        right_df = right_df.rename(columns=rename_map)
        left_col_actual = actual_left_col(j["left_table"], j["left_col"])
        df = df.merge(right_df, how=j.get("join_type", "inner"),
                      left_on=left_col_actual, right_on=right_key)
        if left_col_actual != right_key and right_key in df.columns:
            df = df.drop(columns=[right_key])
        joined_aliases.add(right_alias)
        # Add right-table columns to joined_cols (with prefix where needed).
        # Skip the right-side join key — it's redundant with the left-side key in the join.
        right_table_cfg = next(t for t in tables if t["alias"] == right_alias)
        for c in right_table_cfg["columns"]:
            if c["name"] == right_key:
                continue
            new_name = f"{right_alias}_{c['name']}"
            joined_cols.append({**c, "name": new_name})
    return df, joined_cols


def csv_to_hyper_from_df(df, hyper_path: Path, columns: list[dict]) -> None:
    """Write a pandas DataFrame to a .hyper file, restricted to the listed columns."""
    from csv_to_hyper import _coerce, _TYPE_MAP
    from tableauhyperapi import HyperProcess, Connection, CreateMode, Telemetry, TableDefinition, TableName, SqlType, Nullability, Inserter
    if hyper_path.exists():
        hyper_path.unlink()
    table_def = TableDefinition(
        table_name=TableName("Extract", "Extract"),
        columns=[
            TableDefinition.Column(c["name"], _TYPE_MAP.get(c["datatype"], SqlType.text()), Nullability.NULLABLE)
            for c in columns
        ],
    )
    rows = []
    for _, row in df.iterrows():
        row_out = []
        for c in columns:
            val = row.get(c["name"])
            if val is None or (hasattr(val, "__class__") and val.__class__.__name__ == "float" and val != val):  # NaN
                row_out.append(None)
                continue
            row_out.append(_coerce(str(val), c["datatype"]))
        rows.append(row_out)
    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(endpoint=hyper.endpoint, database=hyper_path, create_mode=CreateMode.CREATE_AND_REPLACE) as conn:
            conn.catalog.create_schema("Extract")
            conn.catalog.create_table(table_def)
            with Inserter(conn, table_def) as inserter:
                inserter.add_rows(rows)
                inserter.execute()


def package_twbx_multi(twb_xml: str, csv_paths: list[Path], hyper_path: Path, output_twbx: Path) -> None:
    output_twbx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_twbx, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{output_twbx.stem}.twb", twb_xml)
        # bundle joined hyper at Data/<primary>_joined.hyper
        primary_stem = csv_paths[0].stem
        zf.write(hyper_path, f"Data/{primary_stem}_joined.hyper")
        # bundle each source CSV
        for p in csv_paths:
            zf.write(p, f"Data/{p.name}")


def _resolve_paths(cfg: dict) -> dict:
    """Make relative paths absolute, anchored at the course/ directory.
    course/ is the parent of this script's directory (course/build/ → course/).
    Absolute paths pass through unchanged."""
    course_root = Path(__file__).resolve().parent.parent
    def _abs(p):
        if not p:
            return p
        pp = Path(p)
        return str(pp if pp.is_absolute() else (course_root / p))
    for k in ("data_csv", "output_twbx"):
        if k in cfg:
            cfg[k] = _abs(cfg[k])
    if "tables" in cfg:
        for t in cfg["tables"]:
            if "csv_path" in t:
                t["csv_path"] = _abs(t["csv_path"])
    return cfg


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: build_twbx.py <config.json>", file=sys.stderr)
        sys.exit(2)
    cfg = json.loads(Path(sys.argv[1]).read_text())
    cfg = _resolve_paths(cfg)
    output = Path(cfg["output_twbx"])
    output.parent.mkdir(parents=True, exist_ok=True)

    # Multi-table mode if 'tables' is in config
    if "tables" in cfg:
        joined_df, joined_columns = build_joined_dataframe_and_columns(cfg)
        primary_csv = Path(cfg["tables"][0]["csv_path"]).resolve()
        hyper_path = output.parent / f".{primary_csv.stem}_joined.hyper.tmp"
        print(f"generating joined extract: {hyper_path}  ({len(joined_df)} rows, {len(joined_columns)} cols)")
        csv_to_hyper_from_df(joined_df, hyper_path, joined_columns)
        twb_xml = build_workbook_multi(cfg, joined_columns)
        csv_paths = [Path(t["csv_path"]).resolve() for t in cfg["tables"]]
        package_twbx_multi(twb_xml, csv_paths, hyper_path, output)
        hyper_path.unlink()
        print(f"wrote {output}  ({output.stat().st_size} bytes)")
        return

    # Single-table mode (existing)
    csv_path = Path(cfg["data_csv"]).resolve()
    from csv_to_hyper import csv_to_hyper
    hyper_path = output.parent / f".{csv_path.stem}.hyper.tmp"
    print(f"generating extract: {hyper_path}")
    csv_to_hyper(csv_path, hyper_path, cfg["columns"])
    twb_xml = build_workbook(cfg)
    package_twbx(twb_xml, csv_path, hyper_path, output)
    hyper_path.unlink()
    print(f"wrote {output}  ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
