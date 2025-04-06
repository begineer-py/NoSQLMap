#!/usr/bin/env python3
"""
NoSQLMap - NoSQL數據庫攻擊工具
"""

import sys
import argparse
from i18n_utils import get_message, set_language
from nosqlmap_modules.main import build_parser, main

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    main(args)
