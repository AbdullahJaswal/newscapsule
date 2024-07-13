#!/bin/sh

# Install Dependencies
pip install -r requirements.txt

# Run Lambda Function
python fetch-wikinews-articles.py
