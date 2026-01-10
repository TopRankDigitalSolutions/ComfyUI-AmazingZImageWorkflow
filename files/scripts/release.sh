#!/usr/bin/env bash
# File    : release.sh
# Purpose : Release script for the Amazing Z-Image Workflow project
# Author  : Martin Rizzo | <martinrizzo@gmail.com>
# Date    : Dec 12, 2025
# Repo    : https://github.com/martin-rizzo/AmazingZImageWorkflow
# License : Unlicense
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           Amazing Z-Image Workflow
#  Z-Image workflow with customizable image styles and GPU-friendly versions
#_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


# Builds a zip file containing specific workflow files and associated images.
#
# Usage:
#   build_zip_file ZIP_FILE WORKFLOW
#
# Parameters:
#   ZIP_FILE: The path to the output zip file.
#   WORKFLOW: The base name of the workflow (e.g., "amazing-z-image").
#
# This function collects several types of files and organizes them into a single
# zip archive. It includes general files like LICENSE, README.TXT, and various
# workflows and galleries with different suffixes and potential variations.
#
# Specifically, it looks for:
#   - "LICENSE"
#   - "files/amazing-z-readme.txt"  (renamed to "README.TXT")
#   - Workflow files           : "${WORKFLOW}<V>_<FORMAT>.json"
#   - Gallery description files: "${WORKFLOW}<V>_gallery.txt"    (renamed to "gallery<V>.txt")
#   - And gallery image files  : "${WORKFLOW}<V>_gallery<N>.jpg" (renamed to "gallery<V><N>.jpg")
#  where:
#    <FORMAT> can be "_GGUF" or "_SAFETENSORS"
#    <V> is a variant (e.g., "-a", "-b")
#    <N> is an integer representing different gallery images (e.g. 1, 2, 3, etc.)
#
# The function creates temporary copies of certain files (like README.TXT and
# gallery files) with appropriate names to archive them within the final zip.
# After creating the zip file, it removes those temporary copies.
#
# Example usage:
#    build_zip_file workflow.zip amazing-z-image
#
#
build_zip_file() {
    local zip_file="$1"
    local workflow="$2"
    local temp_files_=() #< to keep track of temporary files
    local gallery_ext=".jpg"

    # file name suffixes regarding the format of the checkpoint file
    local formats=( "_GGUF" "_SAFETENSORS" )

    # file name suffixes relating to different variants of the same workflow
    local possible_variations=( "" "-a" "-b" "-c" "-d" "-e" "-f" )
    local found_variations=( )

    # in this array, we collect all the files that are part of the release package
    local zip_content=( )

    # collect the file "LICENSE" and "files/amazing-z-readme.txt"
    zip_content+=( LICENSE )
    cp "files/amazing-z-readme.txt" "README.TXT"
    zip_content+=( "README.TXT" )
    temp_files_+=( "README.TXT" )

    # loop through all possible variations that the workflow can have,
    for variation in "${possible_variations[@]}"; do
        local found=
        for format in "${formats[@]}"; do
            local workflow_file="${workflow}${variation}${format}.json"
            [[ ! -f "$workflow_file" ]] && continue

            # if the workflow file exists, then add it to the zip content
            # and mark the variation as found
            zip_content+=( "${workflow_file}" )
            found=true
        done

        # if variation was found, then add it to the list
        if [[ $found == true ]]; then
            found_variations+=( "${variation}" )
        fi
    done

    # for each found variation, creates the temporary gallery files
    # ${variation} is empty string in workflows that don't have variations
    for variation in "${found_variations[@]}"; do

        # ${va} is ${variation} but without prefix '-'
        #local va="${variation#-}"
        #[[ -n "${va}" ]] && va="${va}_"
        local va="${variation}"

        # check if the file "${workflow}_gallery.txt" exists
        gallery_file="${workflow}${variation}_gallery.txt"
        new_file="gallery${va}.txt"
        [[ ! -f "$gallery_file" ]] && continue

        # create the file "$gallery${va}.txt" and add it to the zip content
        cp "$gallery_file" "$new_file"
        zip_content+=( "$new_file" )
        temp_files_+=( "$new_file" )

        # search for files that match "${workflow}_gallery<N>.jpg" pattern,
        # where N is a number between 0 and 9 and {gallery_ext} is always ".jpg"
        for idx in {0..9}; do
            gallery_file="${workflow}${variation}_gallery${idx}${gallery_ext}"
            new_file="gallery${va}${idx}${gallery_ext}"
            [[ ! -f "$gallery_file" ]] && continue

            # create the file "$gallery${va}<N>.jpg" and add it to the zip content
            cp "$gallery_file" "$new_file"
            zip_content+=( "$new_file" )
            temp_files_+=( "$new_file" )
        done
    done

    # create the zip archive with the collected files
    zip -j "$zip_file" "${zip_content[@]}"

    # remove temporary files
    rm "${temp_files_[@]}"
}


# Builds the release package for each workflow
#
# Usage:
#   build_release_packages [VERSION] [OUTPUT_DIR]
#
# Parameters:
#   VERSION    : The version string (e.g., "v1.2.3"). Defaults to "v1.2.3".
#   OUTPUT_DIR : The directory where the ZIP files will be saved. Defaults to "/tmp/amazing_release".
#
# Example:
#   build_release_packages "v1.2.0" "/tmp/amazing_release"
#
build_release_packages() {
    local VERSION=${1:-v1.2.3}
    local OUTPUT_DIR=${2:-/tmp/amazing_release}
    local MAJOR MINOR
    MAJOR=$(echo "${VERSION##v}" | cut -d '.' -f1)
    MINOR=$(echo "${VERSION##v}" | cut -d '.' -f2)

    build_zip_file "$OUTPUT_DIR/amazingZImage_v${MAJOR}${MINOR}.zip"  amazing-z-image
    build_zip_file "$OUTPUT_DIR/amazingZComics_v${MAJOR}${MINOR}.zip" amazing-z-comics
    build_zip_file "$OUTPUT_DIR/amazingZPhoto_v${MAJOR}${MINOR}.zip"  amazing-z-photo
}


#===========================================================================#
#////////////////////////////////// MAIN ///////////////////////////////////#
#===========================================================================#
# The "RELEASE_DIR" variable is exported so it can be used by github workflow.

# generate the release directory taking as base the second argument
# (if the second parameter is not provided, use '/tmp/amazing_release')
export RELEASE_DIR="${2:-/tmp}/amazing_release"
mkdir -p "$RELEASE_DIR"

# calls "build_release_packages"
#  - the first parameter is the version,
#  - the second parameter is the output directory.
build_release_packages "$1" "$RELEASE_DIR"

# prints a message with the location of zip archives
echo
echo "The files were created in: $RELEASE_DIR"
echo
