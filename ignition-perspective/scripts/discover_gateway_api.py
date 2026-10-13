#!/usr/bin/env python3
"""Read a Gateway OpenAPI specification. Never call mutating endpoints."""
import argparse
import ipaddress
import json
import math
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from project_lib import MAX_FILE, ProjectError, parse_json


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ProjectError("Gateway redirected the request; verify the configured URL. Credentials were not forwarded")


def spec_url(base):
    p = urllib.parse.urlsplit(base)
    if p.scheme not in ("http", "https") or not p.hostname or p.username or p.password or p.query or p.fragment:
        raise ProjectError("Use an http(s) Gateway URL without credentials, query or fragment")
    loopback = p.hostname == "localhost"
    try:
        loopback = loopback or ipaddress.ip_address(p.hostname).is_loopback
    except ValueError:
        pass
    if p.scheme == "http" and not loopback:
        raise ProjectError("Non-loopback Gateways require HTTPS")
    path = p.path.rstrip("/")
    if not path.endswith("/openapi.json"):
        path += "/openapi.json"
    return urllib.parse.urlunsplit((p.scheme, p.netloc, path, "", ""))


def fetch_spec(base, token=None, ca_file=None, timeout=15):
    url = spec_url(base)
    context = ssl.create_default_context(cafile=ca_file)
    opener = urllib.request.build_opener(NoRedirect(), urllib.request.HTTPSHandler(context=context))
    headers = {"Accept": "application/json"}
    if token:
        headers["X-Ignition-API-Token"] = token
    try:
        with opener.open(urllib.request.Request(url, headers=headers), timeout=timeout) as response:
            data = response.read(MAX_FILE + 1)
        if len(data) > MAX_FILE:
            raise ProjectError("OpenAPI specification exceeds size limit")
        return parse_json(data, "OpenAPI response")
    except urllib.error.HTTPError as exc:
        raise ProjectError("OpenAPI request returned HTTP {}; check API access and token permissions".format(exc.code)) from exc
    except (urllib.error.URLError, OSError, ValueError) as exc:
        # Avoid echoing credentials, URLs, response bodies or proxy details.
        raise ProjectError("OpenAPI connection failed ({}); check address, TLS trust and reachability".format(type(exc).__name__)) from exc


def summarize(spec):
    if not isinstance(spec, dict) or not isinstance(spec.get("paths"), dict) or not ("openapi" in spec or "swagger" in spec):
        raise ProjectError("Input is not an OpenAPI specification")
    operations = []
    for path, item in sorted(spec["paths"].items()):
        if not isinstance(item, dict):
            continue
        if any(term in path.lower() for term in ("project", "perspective", "resource", "scan")):
            for method, operation in item.items():
                if method.lower() in ("get", "post", "put", "patch", "delete", "head", "options") and isinstance(operation, dict):
                    operations.append({"method": method.upper(), "path": path,
                                       "operationId": operation.get("operationId"),
                                       "summary": operation.get("summary"),
                                       "security": operation.get("security", spec.get("security"))})
    return {"info": spec.get("info", {}), "operations": operations,
            "notes": ["Discovery only; no operations listed here were executed.",
                      "A missing/null security declaration does not prove unauthenticated access; verify Gateway access requirements.",
                      "Inspect parameter and request-body schemas in the original specification before constructing requests.",
                      "Gateway configuration resource APIs and project-resource APIs are distinct; do not infer a view-write endpoint."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Gateway base URL or exact openapi.json URL")
    group.add_argument("--spec", help="Previously saved OpenAPI JSON file")
    parser.add_argument("--token-env", default="IGNITION_API_TOKEN", help="Name of environment variable containing an existing API token")
    parser.add_argument("--ca-file", help="Trusted CA bundle for a private HTTPS Gateway")
    parser.add_argument("--timeout", type=float, default=15)
    args = parser.parse_args()
    try:
        if not math.isfinite(args.timeout) or args.timeout <= 0:
            raise ProjectError("Timeout must be finite and positive")
        if args.spec:
            with Path(args.spec).open("rb") as stream:
                data = stream.read(MAX_FILE + 1)
            if len(data) > MAX_FILE:
                raise ProjectError("Specification exceeds size limit")
            spec = parse_json(data, args.spec)
        else:
            spec = fetch_spec(args.url, os.environ.get(args.token_env), args.ca_file, args.timeout)
        print(json.dumps(summarize(spec), indent=2))
        return 0
    except (ProjectError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
