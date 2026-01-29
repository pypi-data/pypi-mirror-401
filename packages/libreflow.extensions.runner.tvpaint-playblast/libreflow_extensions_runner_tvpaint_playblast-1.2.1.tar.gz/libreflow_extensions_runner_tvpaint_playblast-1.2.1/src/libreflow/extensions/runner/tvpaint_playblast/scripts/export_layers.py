import os
import subprocess
import sys
import argparse
from pytvpaint import george
from pytvpaint.project import Project


def process_remaining_args(args):
    parser = argparse.ArgumentParser(
        description='TVPaint Render Arguments'
    )
    parser.add_argument('--output-path', dest='output_path')
    parser.add_argument('--filter-layers', dest='filter_layers', action="append")
    parser.add_argument('--delete-json', dest='delete_json', action='store_true')

    values, _ = parser.parse_known_args(args)

    return [values.output_path, values.filter_layers, values.delete_json]

OUTPUT_PATH, FILTER_LAYERS, DELETE_JSON = process_remaining_args(sys.argv)

project = Project.current_project()
clip = project.current_clip

layers = None
if FILTER_LAYERS:
    # Get layer objects
    layers = []
    for name in FILTER_LAYERS:
        layer = clip.get_layer(by_name=name)
        if layer:
            layers.append(layer)

# Export layers in image sequence and with layers ordering in a json file
clip.export_json(
    OUTPUT_PATH,
    george.SaveFormat.PNG,
    folder_pattern="%3li_%ln",
    file_pattern="%ln.%4ii",
    layer_selection=layers,
    all_images=True,
)

if DELETE_JSON:
    os.remove(OUTPUT_PATH)

project.close_all(True)