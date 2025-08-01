#!/usr/bin/env bash
set -e

host="$1"
port="$2"
shift 2

echo "⏳ Waiting for $host:$port to be ready..."

until nc -z "$host" "$port"; do
  sleep 1
done

echo "✅ $host:$port is available — continuing"
exec "$@"