#!/bin/bash

BASE_DIR=$(cd $(dirname "$0") && pwd -P)
cd $BASE_DIR

# UTILS
warning() {
    echo "! $@" >&2
}

error() {
    echo "$@" >&2
    exit 2
}

clean_pyc() {
    local retval
    find . -name \*.pyc -print0 | xargs -0 rm -f
    retval=$?
    warning "Removed all *.pyc files from  " >&2
    return $?
}
usage() {
    cat <<EOT
---------------------------
WaterMarker Tester
---------------------------
Runs unittests as well as integration testing

Usage:
full tests          $0
file test           $0 /path/test_file.py
module test         $0 test.module

EOT
}

# Usage print
while getopts ":h" opt; do
    case $opt in
        h)
            usage
            exit 0
            ;;
    esac
done

# CONSTANTS
PYTHON=$(which python) || error "Python 2.7 or later required"
NOSETESTS=$(which nosetests) || error "Nosetests not installed"

clean_pyc || error "Failed to cleanup pyc files"
$NOSETESTS \
    --with-coverage \
    --detailed-errors \
    --logging-level=ERROR \
    --cover-branches \
    --cover-erase \
    --cover-package=watermarker \
    --cover-package=watermark.color \
    --cover-package=watermark.constants \
    --cover-package=watermark.job \
    --cover-package=watermark.utils \
    --cover-package=watermark.validator \
    --cover-package=watermark.workflow \
    "${@:1}"
