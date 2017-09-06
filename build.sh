#!/bin/sh

PYINSTALLER=/usr/local/bin/pyinstaller

# Remove any previous build of the app.
rm -rf build
rm -rf dist

# Train the classifier.
python HistogramClassifier.py

# Build the app.
python "$PYINSTALLER" Luxocator.spec

# Determine the platform.
platform=`uname -s`

if [ "$platform" = 'Darwin' ]; then
    # We are on Mac.
    # Copy custom metadata and resources into the app bundle.
    cp -r mac/Contents dist/Luxocator.app
fi
