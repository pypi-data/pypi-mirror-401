from .string_helpers import camel_to_kebab
from .string_helpers import kebab_to_camel
from .string_helpers import has_mustache
import re
import uuid
import inspect
from typing import Dict, List, Optional, Tuple
from .component_decorator import Component, load_component_from_path
import os


def convert_mustache_attrs_to_kebab_raw(html):
    def replace_attr(match):
        attr_name = match.group(1)
        equals_quote = match.group(2)
        value = match.group(3)
        end_quote = match.group(4)

        if has_mustache(value):
            new_name = camel_to_kebab(attr_name)
            return f'{new_name}{equals_quote}{value}{end_quote}'
        return match.group(0)

    pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)(=["\'])([^"\']*?)(["\'])'
    return re.sub(pattern, replace_attr, html)


def extract_component_original_attrs(html, pattern):
    component_attrs_map = {}

    for match in re.finditer(pattern, html):
        component_name = match.group(1)
        tag_start = match.start()

        remaining = html[tag_start:]
        tag_end_match = re.search(r'/?>', remaining)
        if tag_end_match:
            full_tag = remaining[:tag_end_match.end()]

            attr_pattern = re.compile(
                r'([a-zA-Z_][\w\-]*)\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+)'
            )
            attrs_original = {}
            for attr_match in attr_pattern.finditer(full_tag):
                attr_name = attr_match.group(1)
                attrs_original[attr_name.lower()] = attr_name

            placeholder = f"ppcomponent{component_name.lower()}"
            if placeholder not in component_attrs_map:
                component_attrs_map[placeholder] = []
            component_attrs_map[placeholder].append(attrs_original)

    return component_attrs_map


# ============================================================================
# IMPORT PARSING
# ============================================================================

def extract_imports(html: str) -> List[Dict]:
    """
    Extract all import statements from HTML.

    Supports:
        <!-- @import Test from "./path" -->
        <!-- @import Test from ./path -->  (unquoted)
        <!-- @import Test as MyTest from "./path" -->
        <!-- @import { Button, Input } from "./path" -->
        <!-- @import { Button as Btn, Input as Field } from "./path" -->
    """
    imports = []

    grouped_pattern = r'<!--\s*@import\s*\{([^}]+)\}\s*from\s*["\']?([^"\'>\s]+)["\']?\s*-->'
    grouped_re = re.compile(grouped_pattern)
    for match in grouped_re.finditer(html):
        members = match.group(1)
        path = match.group(2)

        for member in members.split(','):
            member = member.strip()
            if not member:
                continue
            if ' as ' in member:
                parts = member.split(' as ')
                original = parts[0].strip()
                alias = parts[1].strip()
            else:
                original = member
                alias = member
            imports.append({
                'original': original,
                'alias': alias,
                'path': path
            })

    single_pattern = r'<!--\s*@import\s+(?!\{)(\w+)(?:\s+as\s+(\w+))?\s+from\s*["\']?([^"\'>\s]+)["\']?\s*-->'
    single_re = re.compile(single_pattern)
    for match in single_re.finditer(html):
        original = match.group(1)
        alias = match.group(2) or original
        path = match.group(3)
        imports.append({
            'original': original,
            'alias': alias,
            'path': path
        })

    return imports


def strip_imports(html: str) -> str:
    """Remove import comments from HTML"""
    html = re.sub(
        r'<!--\s*@import\s*\{[^}]+\}\s*from\s*["\']?[^"\'>\s]+["\']?\s*-->\n?', '', html
    )
    html = re.sub(
        r'<!--\s*@import\s+\w+(?:\s+as\s+\w+)?\s+from\s*["\']?[^"\'>\s]+["\']?\s*-->\n?', '', html
    )
    return html


def build_alias_map(imports: List[Dict], base_dir: str = "") -> Dict[str, Component]:
    """Build mapping from alias names to Component instances."""
    alias_map = {}

    for imp in imports:
        original = imp['original']
        alias = imp['alias']
        path = imp['path']

        component = load_component_from_path(path, original, base_dir)
        if component:
            alias_map[alias] = component

    return alias_map


def process_imports(html: str, base_dir: str = "") -> tuple[str, Dict[str, Component]]:
    """Process imports and return cleaned HTML with alias map."""
    imports = extract_imports(html)
    alias_map = build_alias_map(imports, base_dir)
    cleaned_html = strip_imports(html)
    return cleaned_html, alias_map


# ============================================================================
# COMPONENT HELPERS
# ============================================================================

def needs_parent_scope(attrs):
    for key, value in attrs.items():
        if key.lower().startswith('on'):
            return True
        if has_mustache(value):
            return True
    return False


def wrap_scope(html, scope):
    return f'<!-- pp-scope:{scope} -->{html}<!-- /pp-scope -->'


def accepts_children(fn):
    sig = fn.__signature__ if isinstance(
        fn, Component) else inspect.signature(fn)
    params = sig.parameters
    return 'children' in params or any(
        p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()
    )


def _event_listener_props(props: Dict[str, str]) -> Dict[str, str]:
    """Return only event-listener props (React style: onClick, onChange, ...)."""
    out: Dict[str, str] = {}
    for k, v in props.items():
        if k.lower().startswith("on"):
            out[k] = v
    return out


def _event_attr_names(event_prop: str) -> Tuple[str, str]:
    """Return (camelCaseName, kebab-case-name) for an event prop."""
    return event_prop, camel_to_kebab(event_prop)


def _find_matching_closing_tag(html: str, tag: str, start_pos: int) -> Optional[int]:
    """
    Find the start index of the closing tag for the first opened <tag> after start_pos.
    Handles nested tags of the same name; best-effort, not a full HTML parser.
    """
    tag_re = re.compile(rf"<(/?){re.escape(tag)}\b", re.IGNORECASE)
    depth = 1
    pos = start_pos

    while True:
        m = tag_re.search(html, pos)
        if not m:
            return None

        # Skip comment blocks
        if html.startswith("<!--", m.start()):
            endc = html.find("-->", m.start() + 4)
            pos = (endc + 3) if endc != -1 else (m.start() + 4)
            continue

        gt = html.find(">", m.start())
        if gt == -1:
            return None
        seg = html[m.start():gt + 1]

        is_closing = (m.group(1) == "/")
        is_self_closing = (not is_closing) and seg.rstrip().endswith("/>")

        if is_closing:
            depth -= 1
            if depth == 0:
                return m.start()
        elif not is_self_closing:
            depth += 1

        pos = gt + 1


# Tags whose inner content is treated as text (RCDATA / raw text behavior).
# Injecting HTML comments *inside* these will turn into textarea/title text and get entity-escaped.
_RAWTEXT_ROOT_TAGS = {"textarea", "title"}


def _inject_component_scope_inside_root(html: str, component_scope: str) -> str:
    """
    Inject component scope comments *inside* the root element.
    This is used only when the parent must own the root tag/attrs (prop/event expressions),
    but the component body must run under component scope.

    IMPORTANT: Skip raw-text roots (e.g., textarea/title), otherwise comments become text.
    """
    s = str(html).strip()
    if not s:
        return s

    i = 0
    while True:
        lt = s.find("<", i)
        if lt == -1:
            return wrap_scope(s, component_scope)

        if s.startswith("<!--", lt) or s.startswith("<!", lt) or s.startswith("<?", lt):
            i = lt + 2
            continue

        m = re.match(r"<([a-zA-Z][\w:-]*)\b[^>]*>", s[lt:])
        if not m:
            i = lt + 1
            continue

        tag = m.group(1)
        tag_l = tag.lower()
        open_end = lt + m.end()
        open_seg = s[lt:open_end]

        # Do not inject inside raw-text roots
        if tag_l in _RAWTEXT_ROOT_TAGS:
            return wrap_scope(s, component_scope)

        # Self-closing root cannot contain injection
        if open_seg.rstrip().endswith("/>"):
            return wrap_scope(s, component_scope)

        close_start = _find_matching_closing_tag(s, tag, open_end)
        if close_start is None:
            return wrap_scope(s, component_scope)

        open_comment = f"<!-- pp-scope:{component_scope} -->"
        close_comment = "<!-- /pp-scope -->"
        return s[:open_end] + open_comment + s[open_end:close_start] + close_comment + s[close_start:]


def _wrap_event_elements_with_parent_scope(html: str, event_listeners: Dict[str, str], parent_scope: str) -> str:
    """
    Best-effort: wrap the element(s) that use a specific passed-in handler value
    with the parent's scope. Mirrors PHP wrapEventElementsWithScope behavior.
    """
    if not event_listeners or not parent_scope:
        return str(html)

    s = str(html)
    wraps: List[Tuple[int, int, str]] = []

    for event_prop, handler in event_listeners.items():
        camel_name, kebab_name = _event_attr_names(event_prop)

        attr_pat = re.compile(
            rf"<([a-zA-Z][\w:-]*)\b[^>]*\s(?:{re.escape(camel_name)}|{re.escape(kebab_name)})\s*=\s*(\"([^\"]*)\"|'([^']*)')[^>]*>",
            re.IGNORECASE,
        )

        for m in attr_pat.finditer(s):
            val = m.group(3) if m.group(3) is not None else (m.group(4) or "")
            if val != handler:
                continue

            tag = m.group(1)
            start = m.start()
            open_end = m.end()

            # Self-closing tag: wrap the tag itself
            if s[start:open_end].rstrip().endswith("/>"):
                wraps.append((start, open_end, wrap_scope(
                    s[start:open_end], parent_scope)))
                continue

            close_start = _find_matching_closing_tag(s, tag, open_end)
            if close_start is None:
                continue
            close_end = s.find(">", close_start)
            if close_end == -1:
                continue
            close_end += 1

            wraps.append((start, close_end, wrap_scope(
                s[start:close_end], parent_scope)))

    if not wraps:
        return s

    for start, end, repl in sorted(wraps, key=lambda x: x[0], reverse=True):
        s = s[:start] + repl + s[end:]

    return s


def _get_root_tag_name(fragment: str) -> str:
    m = re.match(r"\s*<([a-zA-Z][\w:-]*)\b", str(fragment).strip())
    return m.group(1).lower() if m else ""


# ============================================================================
# RAW BLOCK PROTECTION (SCRIPT/STYLE)
# ============================================================================

_RAW_TAGS_DEFAULT = ("script", "style")


def _mask_raw_blocks(html: str, tags: Tuple[str, ...] = _RAW_TAGS_DEFAULT) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Replace <script>...</script> and <style>...</style> blocks with tokens.
    Prevents component/import scanning from touching JS/CSS content.
    """
    blocks: List[Tuple[str, str]] = []

    for tag in tags:
        pattern = re.compile(
            rf'<{tag}\b[^>]*>[\s\S]*?</{tag}\s*>',
            re.IGNORECASE
        )

        def repl(m):
            token = f"__PP_RAW_{tag.upper()}_{uuid.uuid4().hex}__"
            blocks.append((token, m.group(0)))
            return token

        html = pattern.sub(repl, html)

    return html, blocks


def _unmask_raw_blocks(html: str, blocks: List[Tuple[str, str]]) -> str:
    for token, original in blocks:
        html = html.replace(token, original)
    return html


# ============================================================================
# MAIN TRANSFORM
# ============================================================================

def transform_components(
    html: str,
    parent_scope: str = "app",
    base_dir: str = "",
    alias_map: Optional[Dict[str, Component]] = None,
    _depth: int = 0
) -> str:
    """
    Transform custom component tags. Components MUST be imported to be resolved.
    Recursively processes component outputs.

    Scoping model (React-like):
      - Each component instance gets its own scope (unique_id).
      - Component template is compiled under its own scope (unique_id).
      - Children are evaluated under the parent scope (wrapped before passing).
      - If parent passes dynamic props/events, the root tag/attrs are evaluated in
        parent scope, while the component body runs in component scope via an
        injected scope section.

    Guarantees:
      - Content inside <script> and <style> tags is never scanned/rewritten.
      - No scope comments are injected inside <textarea> (or other raw-text roots),
        preventing HTML entity escaping inside textarea value.
    """
    if _depth > 50:
        return html

    # 0. Mask script/style blocks so nothing inside them is processed
    html, raw_blocks = _mask_raw_blocks(html, tags=_RAW_TAGS_DEFAULT)

    # 1. Process imports for the current level (safe: scripts/styles are masked)
    html, local_alias_map = process_imports(html, base_dir)

    merged_map = {**(alias_map or {}), **local_alias_map}

    # If no components are imported, return original HTML (but restore raw blocks)
    if not merged_map:
        return _unmask_raw_blocks(html, raw_blocks)

    # 2. Convert mustache attributes to kebab-case (safe: scripts/styles are masked)
    html = convert_mustache_attrs_to_kebab_raw(html)

    # 3. Process components iteratively
    max_iterations = 100
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        component_pattern = r'<([A-Z][a-zA-Z0-9]*)([^>]*?)(?:/>|>([\s\S]*?)</\1>)'

        match = None
        for m in re.finditer(component_pattern, html):
            tag_name = m.group(1)
            if tag_name in merged_map:
                inner_content = m.group(3) or ""
                # Prefer leaf-most component first
                if not re.search(r'<[A-Z][a-zA-Z0-9]*[^>]*(?:/>|>)', inner_content):
                    match = m
                    break
                elif match is None:
                    match = m

        if not match:
            break

        tag_name = match.group(1)
        attrs_str = match.group(2) or ""
        children = match.group(3) or ""

        component_fn = merged_map.get(tag_name)
        if not component_fn:
            break

        # 4. Parse attributes
        props: Dict[str, str] = {}
        attr_pattern = r'([a-zA-Z_][\w\-]*)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|(\S+))'
        for attr_match in re.finditer(attr_pattern, attrs_str):
            attr_name = attr_match.group(1)
            attr_value = attr_match.group(2) or attr_match.group(
                3) or attr_match.group(4) or ""
            camel_name = kebab_to_camel(attr_name)
            props[camel_name] = attr_value

        # Handle boolean attributes (no value)
        bool_attr_pattern = r'\s([a-zA-Z_][\w\-]*)(?=\s|/?>|$)(?!=)'
        for bool_match in re.finditer(bool_attr_pattern, attrs_str):
            attr_name = bool_match.group(1)
            if kebab_to_camel(attr_name) not in props:
                props[kebab_to_camel(attr_name)] = ""

        # Each component instance gets its own scope id
        unique_id = f"{tag_name.lower()}_{uuid.uuid4().hex[:8]}"

        # 5. Add children if component accepts them (children must run in parent scope)
        if children.strip() and accepts_children(component_fn):
            props['children'] = wrap_scope(children, parent_scope)

        # 6. Render the component
        component_html = component_fn(**props)

        # 7. Recursive transform inside the component: compile under component scope
        # (nested component templates evaluate within the current component instance scope)
        if hasattr(component_fn, 'source_path') and component_fn.source_path:
            component_dir = os.path.dirname(component_fn.source_path)
            component_html = transform_components(
                component_html,
                parent_scope=unique_id,
                base_dir=component_dir,
                _depth=_depth + 1
            )

        # 8. Add pp-component attribute to root element
        component_html = re.sub(
            r'^(\s*<[a-zA-Z][a-zA-Z0-9]*)',
            rf'\1 pp-component="{unique_id}"',
            str(component_html).strip(),
            count=1
        )

        # 9. Apply scoping rules
        root_tag = _get_root_tag_name(component_html)
        needs_parent = needs_parent_scope(props)
        event_listeners = _event_listener_props(props)

        if root_tag in _RAWTEXT_ROOT_TAGS:
            # Never inject inside raw-text roots (textarea/title).
            # If parent must own scope (prop/event expressions), keep parent scope.
            # Otherwise, scope the component itself (outside) with unique_id.
            if needs_parent and parent_scope:
                component_html = wrap_scope(component_html, parent_scope)
            else:
                component_html = wrap_scope(component_html, unique_id)
        else:
            if needs_parent and parent_scope:
                # Parent owns root tag/attrs; component body owns internal template
                component_html = _inject_component_scope_inside_root(
                    component_html, unique_id)

                # Wrap event target elements with parent scope (best-effort)
                if event_listeners:
                    component_html = _wrap_event_elements_with_parent_scope(
                        component_html,
                        event_listeners=event_listeners,
                        parent_scope=parent_scope,
                    )

                # Wrap whole component with parent scope (so root attrs resolve in parent)
                component_html = wrap_scope(component_html, parent_scope)
            else:
                # Normal: entire component runs in its own scope (root attrs included)
                component_html = wrap_scope(component_html, unique_id)

        # 10. Replace original tag with transformed result
        html = html[:match.start()] + component_html + html[match.end():]

    # Restore script/style blocks exactly as they were
    html = _unmask_raw_blocks(html, raw_blocks)
    return html
