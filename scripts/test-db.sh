#!/bin/sh
# Applies supabase/migrations to a throwaway local Postgres and runs the RLS scenarios in supabase/tests.
# Needs Postgres binaries (initdb, pg_ctl, psql). Usage: sh scripts/test-db.sh
set -e
BIN=${PG_BIN:-$(ls -d /usr/lib/postgresql/*/bin 2>/dev/null | tail -1)}
DIR=$(mktemp -d /var/tmp/tipulit-pg.XXXX); PORT=${PG_PORT:-54331}
RUN="sh -c"; [ "$(id -u)" = 0 ] && { chown postgres "$DIR"; RUN="su postgres -c"; }
$RUN "$BIN/initdb -D $DIR/data -A trust -U postgres >/dev/null && $BIN/pg_ctl -D $DIR/data -o '-p $PORT -k $DIR' -l $DIR/log -w start >/dev/null"
trap "$RUN '$BIN/pg_ctl -D $DIR/data -m fast stop >/dev/null'; rm -rf $DIR" EXIT
P="$BIN/psql -h $DIR -p $PORT -U postgres -v ON_ERROR_STOP=1 -q"
$P -c "create database t" >/dev/null
$P -d t -f supabase/tests/supabase-stub.sql >/dev/null
for f in supabase/migrations/*.sql; do $P -d t -f "$f" 2>&1 | grep -v NOTICE || true; done
for f in supabase/tests/rls-*.sql; do echo "== $f"; $P -d t -f "$f" 2>&1 | grep -E "OK |FAIL|ERROR" | sed 's/^.*NOTICE:  //'; done
