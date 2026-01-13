#!/bin/bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

set -e

COVERAGE=0
REPORT=0
VERBOSE=0
SPECIFIC_TEST=""

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --coverage)
      COVERAGE=1
      shift
      ;;
    --report)
      REPORT=1
      shift
      ;;
    --verbose)
      VERBOSE=1
      shift
      ;;
    *)
      SPECIFIC_TEST="$1"
      shift
      ;;
  esac
done

CMD="pytest"

if [ $VERBOSE -eq 1 ]; then
  CMD="$CMD -v"
fi

if [ $COVERAGE -eq 1 ]; then
  CMD="$CMD --cov=amazon_bedrock_knowledge_base_mcp"

  if [ $REPORT -eq 1 ]; then
    CMD="$CMD --cov-report=html"
  fi
fi

if [ -n "$SPECIFIC_TEST" ]; then
  CMD="$CMD $SPECIFIC_TEST"
else
  CMD="$CMD tests/"
fi

echo "Running: $CMD"
$CMD

if [ $COVERAGE -eq 1 ] && [ $REPORT -eq 1 ]; then
  echo "Coverage report generated in htmlcov/ directory"
  echo "Open htmlcov/index.html in your browser to view the report"
fi
