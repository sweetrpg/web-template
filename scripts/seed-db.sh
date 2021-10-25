#!/bin/bash

set -x
set -e
set -o pipefail

env_file=${1:.env}

export $(cat $env_file | xargs)

psql -f seed-data/some-file.sql
