#!/bin/bash

gunicorn --config gunicorn.py core.wsgi
