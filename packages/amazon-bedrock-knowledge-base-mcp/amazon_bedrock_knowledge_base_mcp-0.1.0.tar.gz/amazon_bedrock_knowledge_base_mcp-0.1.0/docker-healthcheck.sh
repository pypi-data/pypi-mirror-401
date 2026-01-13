#!/bin/sh

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Modifications Copyright (c) 2026 Zlash65

SERVER="amazon-bedrock-knowledge-base-mcp"

if pgrep -P 0 -a -l -x -f "/app/.venv/bin/python3 /app/.venv/bin/$SERVER" > /dev/null; then
  echo -n "$SERVER is running";
  exit 0;
fi;

exit 1;
