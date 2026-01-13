#!/usr/bin/env python3
import argparse
import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse

__version__ = "1.4.1"

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[38;5;32m'
RESET = '\033[0m'

ENDPOINTS = [
    "api/v3/graphql", "graphql/v3", "api/v4/graphql", "graphql/v4", "v3/graphql",
    "v4/graphql", "api/v3", "api/v4", "v3/api", "v4/api", "v3/api/v1", "v3/api/v2",
    "v4/api/v1", "v4/api/v2", "graphql/v3/api", "graphql/v4/api", "v3/graphql/api",
    "v4/graphql/api", "api/v3/graphql/v1", "api/v4/graphql/v2", "v1/api/graphql/v3",
    "v2/api/graphql/v4", "v3/graphql/v1/api", "v4/graphql/v2/api", "v1/graphql/v3/api",
    "v2/graphql/v4/api", "v3/api/graphql/v1", "v4/api/graphql/v2", "graphql/v1/api/v3",
    "graphql/v2/api/v4", "graphql", "api/graphql", "v1/graphql", "v2/graphql", "api",
    "graphql/api", "v1/api", "v2/api", "graphql/v1", "graphql/v2", "api/v1/graphql",
    "api/v2/graphql", "v1/api/graphql", "v2/api/graphql", "v1", "v2", "api/v1", "api/v2",
    "v1/api/v1", "v1/api/v2", "v2/api/v1", "v2/api/v2", "graphql/v1/api", "graphql/v2/api",
    "v1/graphql/api", "v2/graphql/api", "api/v1/graphql/v1", "api/v2/graphql/v2",
    "v1/api/graphql/v1", "v2/api/graphql/v2", "graphiql", "graphql/query"
]

INTROSPECTION_QUERY = {
    "query": """
    query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          name
          kind
          description
        }
      }
    }
    """
}

TARGET_CONCURRENCY = 20
ENDPOINT_CONCURRENCY = 20


def Banner():
    print(rf"""
  ________                    .__   __________                            
 /  _____/___________  ______ |  |__\______   \ ____   ____  ____   ____  
/   \  __\_  __ \__  \ \____ \|  |  \|       _// __ \_/ ___\/  _ \ /    \ 
\    \_\  \  | \// __ \|  |_> >   Y  \    |   \  ___/\  \__(  <_> )   |  \
 \______  /__|  (____  /   __/|___|  /____|_  /\___  >\___  >____/|___|  /
        \/           \/|__|        \/       \/     \/     \/           \/ 
                                                                v{__version__}
                            {GREEN}pentestproject{RESET}
""")


def normalize_target(line: str) -> str | None:
    s = line.strip()
    if not s or s.startswith("#"):
        return None

    s = s.replace("\x00", "").strip()

    if s.startswith(("http://", "https://")):
        p = urlparse(s)
        host = p.netloc.strip()
        if not host:
            return None
        return host

    if "/" in s:
        s = s.split("/", 1)[0].strip()

    s = s.strip().strip(".")
    if not s:
        return None

    return s


def read_targets_from_file(path):
    seen = set()
    targets = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            t = normalize_target(raw)
            if not t:
                continue
            if t in seen:
                continue
            seen.add(t)
            targets.append(t)

    return targets


async def check_site(session, url):
    try:
        async with session.get(url, allow_redirects=True) as resp:
            print(f"{BLUE}[+] Site reachable → {url} ({resp.status}){RESET}")
            return True
    except Exception:
        return False


async def scan_base(session, base_url, found, ep_concurrency: int):
    PAYLOAD = {"query": "{ __typename }"}
    semaphore = asyncio.Semaphore(ep_concurrency)

    async def scan(ep):
        full_url = urljoin(base_url.rstrip("/") + "/", ep)
        async with semaphore:
            try:
                async with session.post(full_url, json=PAYLOAD) as resp:
                    ct = resp.headers.get("Content-Type", "")
                    print(f"[DEBUG] {full_url} → {resp.status} | {ct}")
                    if "application/json" in ct:
                        data = await resp.json(content_type=None)
                        if isinstance(data, dict) and ("data" in data or "errors" in data):
                            if full_url not in found:
                                found.add(full_url)
                                print(f"{GREEN}[+] GraphQL FOUND → {full_url}{RESET}")
            except Exception:
                pass

    await asyncio.gather(*(scan(ep) for ep in ENDPOINTS))


async def fetch_schema(session, graphql_url):
    try:
        async with session.post(graphql_url, json=INTROSPECTION_QUERY) as resp:
            if resp.status != 200:
                print(f"{RED}[-] Introspection failed ({resp.status}){RESET}")
                return

            data = await resp.json(content_type=None)
            if isinstance(data, dict) and "data" in data and "__schema" in data["data"]:
                schema = data["data"]["__schema"]
                print(f"{GREEN}[+] Schema extracted from {graphql_url}{RESET}")
                for t in schema.get("types", []):
                    print(f"  - {t.get('name')} ({t.get('kind')})")
            else:
                print(f"{YELLOW}[*] Introspection disabled → {graphql_url}{RESET}")

    except Exception as e:
        print(f"{RED}[-] Schema error → {e}{RESET}")


async def GraphQLScanner(
    target: str,
    fetch_schema_flag: bool,
    ep_concurrency: int,
    interactive_schema_prompt: bool = True
):
    """
    interactive_schema_prompt:
      - True  => your original behavior: prompt per found endpoint (best for single target)
      - False => do not prompt (useful for --list scans). Still returns found endpoints.
    """
    found = set()

    if target.startswith(("http://", "https://")):
        base_urls = [target]
    else:
        base_urls = [f"https://{target}"]

    timeout = aiohttp.ClientTimeout(total=8)
    connector = aiohttp.TCPConnector(ssl=False, limit=50)
    headers = {
        "Content-Type": "application/json",
        "User-Agent": f"GraphRecon/{__version__}"
    }

    async with aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
        headers=headers
    ) as session:

        for base_url in base_urls:
            if not await check_site(session, base_url):
                continue

            await scan_base(session, base_url, found, ep_concurrency)

        if not found:
            print(f"{RED}[-] GraphQL NOT FOUND{RESET}")
            return set()

        if fetch_schema_flag and interactive_schema_prompt:
            for graphql_url in sorted(found):
                choice = input(
                    f"{GREEN}[?] Schema found at {graphql_url}. Fetch schema? (y/N): {RESET}"
                ).strip().lower()

                if choice == "y":
                    await fetch_schema(session, graphql_url)
                else:
                    print(f"{YELLOW}[*] Skipped {graphql_url}{RESET}")

    return found


async def fetch_schemas_after_bulk(schema_urls: set[str]):
    """
    After bulk scan, optionally fetch schemas for all discovered GraphQL endpoints.
    """
    if not schema_urls:
        return

    choice = input(
        f"{GREEN}[?] Bulk scan finished. {len(schema_urls)} GraphQL endpoints found. Fetch schemas now? (y/N): {RESET}"
    ).strip().lower()

    if choice != "y":
        print(f"{YELLOW}[*] Skipped schema fetching{RESET}")
        return

    timeout = aiohttp.ClientTimeout(total=12)
    connector = aiohttp.TCPConnector(ssl=False, limit=50)
    headers = {
        "Content-Type": "application/json",
        "User-Agent": f"GraphRecon/{__version__}"
    }

    async with aiohttp.ClientSession(timeout=timeout, connector=connector, headers=headers) as session:
        for u in sorted(schema_urls):
            print(f"{BLUE}[*] Fetching schema → {u}{RESET}")
            await fetch_schema(session, u)


async def run_targets_concurrently(
    targets,
    fetch_schema_flag: bool,
    tconcurrency: int,
    ep_concurrency: int
):
    sem = asyncio.Semaphore(tconcurrency)
    all_found_graphql_urls: set[str] = set()

    async def runner(t, idx: int):
        async with sem:
            print(f"{YELLOW}[*] ({idx}/{len(targets)}) Scanning target: {t}{RESET}")
            found = await GraphQLScanner(
                t,
                fetch_schema_flag=fetch_schema_flag,
                ep_concurrency=ep_concurrency,
                interactive_schema_prompt=False
            )
            if found:
                all_found_graphql_urls.update(found)

    await asyncio.gather(*(runner(t, i + 1) for i, t in enumerate(targets)))

    if fetch_schema_flag and all_found_graphql_urls:
        await fetch_schemas_after_bulk(all_found_graphql_urls)


async def async_main():
    Banner()
    parser = argparse.ArgumentParser(description="Async GraphQL scanner")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="Target domain or URL")
    group.add_argument("-l", "--list", help="Path to txt file containing targets (one per line)")

    parser.add_argument("--schema", action="store_true", help="Try to fetch GraphQL schema")

    args = parser.parse_args()

    print(f"{YELLOW}[*] Scanning is starting{RESET}")

    if args.list:
        targets = read_targets_from_file(args.list)
        if not targets:
            print(f"{RED}[-] Target list is empty or unreadable{RESET}")
            return

        print(f"{BLUE}[+] Loaded {len(targets)} unique targets from {args.list}{RESET}")
        await run_targets_concurrently(
            targets,
            fetch_schema_flag=args.schema,
            tconcurrency=TARGET_CONCURRENCY,
            ep_concurrency=ENDPOINT_CONCURRENCY
        )
    else:
        await GraphQLScanner(
            args.url,
            fetch_schema_flag=args.schema,
            ep_concurrency=ENDPOINT_CONCURRENCY,
            interactive_schema_prompt=True
        )


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()