#!/usr/bin/env bash
# File    : release.sh
# Purpose : Release script for the AmazingZImageWorkflow project
# Author  : Martin Rizzo | <martinrizzo@gmail.com>
# Date    : Dec 12, 2025
# Repo    : https://github.com/martin-rizzo/AmazingZImageWorkflow
# License : Unlicense2
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           Amazing Z-Image Workflow
#  Z-Image workflow with customizable image styles and GPU-friendly versions
#_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


zip_z_comics() {
    local PACKAGE=${1:-1}
    local VERSION=${2:-v1.0.0}
    local TEMP_DIR=${3:-/tmp}
    local OUTPUT_DIR="$TEMP_DIR/amazing_release"

    # este valor es retornado (no es local)
    export ZIP_PATH="$OUTPUT_DIR/amazing-z-comics.zip"

    # busca amazing-z-comics_GGUF.json y amazin-z-comics_SAFETENSORS.json en el directorio actual
    # y los empaquete en un zip en el directorio OUTPUT_DIR
    mkdir -p "$OUTPUT_DIR"
    zip -j "$ZIP_PATH" "amazing-z-comics_GGUF.json" "amazing-z-comics_SAFETENSORS.json"
}

zip_z_image() {
    local PACKAGE=${1:-1}
    local VERSION=${2:-v1.0.0}
    local TEMP_DIR=${3:-/tmp}
    local OUTPUT_DIR="$TEMP_DIR/amazing_release"

    # este valor es retornado (no es local)
    export ZIP_PATH="$OUTPUT_DIR/amazing-z-image.zip"

    # busca amazing-z-comics_GGUF.json y amazin-z-comics_SAFETENSORS.json en el directorio actual
    # y los empaquete en un zip en el directorio OUTPUT_DIR
    mkdir -p "$OUTPUT_DIR"
    zip -j "$ZIP_PATH" "amazing-z-image_GGUF.json" "amazing-z-image_SAFETENSORS.json"
}


#===========================================================================#
#////////////////////////////////// MAIN ///////////////////////////////////#
#===========================================================================#

if [[ "$1" == 'z-comics' ]]; then
    zip_z_comics "$@"
elif [[ "$1" == 'z-image' || -z "$1" ]]; then
    zip_z_image "$@"
else
    echo "Usage: release.sh [z-comics|z-image] <version> <temp_dir>"
fi
