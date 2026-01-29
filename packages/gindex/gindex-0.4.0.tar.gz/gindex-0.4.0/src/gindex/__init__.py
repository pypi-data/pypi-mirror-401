#!/usr/bin/python3
# vim: set ts=4
#
# Copyright 2026-present Linaro Limited
#
# Author: Rémi Duraffort <remi.duraffort@linaro.org>
#
# SPDX-License-Identifier: MIT

import argparse
import shutil
import sys
from pathlib import Path

import gdown


##########
# Setups #
##########
def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Google Drive index builder")

    parser.add_argument("did", help="Google drive id")
    parser.add_argument("output", type=Path, help="Output directory")
    return parser


########
# Data #
########
HEADER = """<!DOCTYPE html>
<html lang="en" translate="no">
  <head>

    <title>Drive artifacts</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/solid.css" integrity="sha384-v2Tw72dyUXeU3y4aM2Y0tBJQkGfplr39mxZqlTBDUZAb9BGoC40+rdFCG0m10lXk" crossorigin="anonymous">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.8/css/fontawesome.css" integrity="sha384-q3jl8XQu1OpdLgGFvNRnPdj5VIlCvgsDQTQB6owSOHWlAurxul7f+JpUOVdAiJ5P" crossorigin="anonymous">
  <link rel="stylesheet" href="/static/styles.css">
  <link rel="icon" href="data:;base64,=">
  <meta name="google" content="notranslate" />

  </head>
  <body>
    <div class="container">
      <div class="col-12-xs">
	    <h3></h3>
        <table class="table table-striped">
          <tr>
            <th></th>
            <th>Filename</th>
            <th>Drive Id</th>
          </tr>
"""

FOOTER = """
      </table>
      </div>
    </div>

    <!-- Footer -->
    <hr>
    <div id="footer">
      <div class="container">
        <p class="text-muted text-center"><a href="https://gitlab.com/ivoire/gindex">gindex</a> 0.4.0, by <a href="https://linaro.org">Linaro</a>.<br />
        </p>
      </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
  </body>
</html>"""


##############
# Entrypoint #
##############
def main() -> int:
    parser = setup_parser()
    options = parser.parse_args()

    shutil.rmtree(options.output, ignore_errors=True)

    print("Listing files")
    files = gdown.download_folder(id=options.did, quiet=True, skip_download=True)

    if len(files) >= 1000:
        print("Too many files, gitlab only accept up to 1000 redirects")
        return 1
    directories = set()

    for file in files:
        print(file.path)
        path = Path(file.path)
        directories.update(path.parents)

    directories = sorted(directories)

    print("")
    print("Creating directory listings")
    for d in directories:
        (options.output / d).mkdir(parents=True)
        data = HEADER

        print(f"* {d}")
        if d.parent != d:
            data += """          <tr>
            <td width="10"><i class="fas fa-arrow-up"></i></td>
            <td><a href="../">Parent Directory</a></td>
            <td></td>
          </tr>"""

        for sd in directories:
            if sd.parent == d and sd != d:
                data += f"""          <tr>
            <td width="10"><i class="fas fa-folder-open"></i></td>
            <td><a href="{sd.name}">{sd.name}/</a></td>
            <td></td>
          </tr>
"""
        for f in files:
            fp = Path(f.path)
            if fp.parent == d:
                data += f"""          <tr>
            <td><i class="fas fa-file"></i></td>
            <td><a href="{fp.name}">{fp.name}</a></td>
            <td><a href="https://drive.usercontent.google.com/download?id={f.id}">{f.id}</td>
          </tr>
"""
        data += FOOTER
        (options.output / d / "index.html").write_text(data)

    print("")
    print(f"Creating _redirects file ({len(files)} files)")
    with (options.output / "_redirects").open("w") as f_out:
        for file in files:
            print(f"* {file.path} => {file.id}")
            f_out.write(
                f"/{file.path} https://drive.usercontent.google.com/download?id={file.id}&confirm=xxx\n"
            )

    return 0
