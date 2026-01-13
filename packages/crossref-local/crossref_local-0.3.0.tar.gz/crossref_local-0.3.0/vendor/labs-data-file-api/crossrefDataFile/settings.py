#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2025-08-22 18:58:46 (ywatanabe)"
# File: /mnt/nas_ug/crossref_local/labs-data-file-api/crossrefDataFile/settings.py
# ----------------------------------------
from __future__ import annotations
import os
__FILE__ = (
    "./labs-data-file-api/crossrefDataFile/settings.py"
)
__DIR__ = os.path.dirname(__FILE__)
# ----------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "your-secret-key-here"

DEBUG = True

# ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "169.254.11.50", "localhost"]


INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "crossrefDataFile",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "crossref.db"),
    }
}

ROOT_URLCONF = "crossrefDataFile.urls"

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# EOF
