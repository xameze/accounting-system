"""Корневой conftest.py — добавляет корень проекта в sys.path для pytest."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
