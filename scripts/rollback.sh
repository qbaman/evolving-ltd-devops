#!/usr/bin/env bash
set -euo pipefail

tag="${1:?Usage: scripts/rollback.sh <known-good-image-tag> [host-port]}"
port="${2:-8080}"
image="evolving-ltd-demo:${tag}"
container="evolving-ltd-test"

if ! [[ "$port" =~ ^[0-9]+$ ]] || (( port < 1 || port > 65535 )); then
  echo "host-port must be an integer from 1 to 65535" >&2
  exit 2
fi

docker image inspect "$image" >/dev/null
if docker container inspect "$container" >/dev/null 2>&1; then
  docker rm --force "$container" >/dev/null
fi

docker run --detach \
  --name "$container" \
  --restart unless-stopped \
  --publish "127.0.0.1:${port}:80" \
  "$image"

for attempt in {1..10}; do
  if curl --fail --silent --show-error --max-time 3 "http://127.0.0.1:${port}/" >/dev/null; then
    echo "Rollback to $image is serving HTTP successfully."
    exit 0
  fi
  sleep 2
done

docker logs "$container" >&2 || true
echo "Rollback image did not pass the local HTTP check." >&2
exit 1
