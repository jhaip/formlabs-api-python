"""
Given a .form file and a base .fps file, generates variants of print settings to optimize for speed
(at the possible expense of print quality).

Example Usage:
python3 examples/speedrun.py test.form --reduce_wiping --reduce_exposure

Known Limitations:
- Changing wiping behavior does not change the estimated print time, although it would increase actual print times
- Only tested on Form 4 printers. Other printer types should work, but may have less accurate print times.

Written by Jacob Haip
"""
import argparse
import json
import os
import sys
import copy
import difflib
import pathlib
import itertools
import uuid
import formlabs_local_api as formlabs


# pathToPreformServer = None
# if sys.platform == 'win32':
#     pathToPreformServer = pathlib.Path().resolve() / "PreFormServer.exe"
# elif sys.platform == 'darwin':
#     pathToPreformServer = pathlib.Path().resolve() / "PreFormServer.app/Contents/MacOS/PreFormServer"
# else:
#     print("Unsupported platform")
#     sys.exit(1)
pathToPreformServer = "/Users/haip/code/Preform/cmake-build-release/app/PreFormServer/output/PreFormServer.app/Contents/MacOS/PreFormServer"

def main():
    args = parse_args()

    report_data = []
    with formlabs.PreFormApi.start_preform_server(pathToPreformServer=pathToPreformServer) as preform:
        # Load the base .form file and get the estimated print time
        print(f"Loading form file {args.form_file}")
        preform.api.load_form_post(formlabs.LoadFormPostRequest(file=args.form_file))
        print("Estimating print time")
        base_estimated_print_time_s = preform.api.scene_estimate_print_time_post().total_print_time_s

        base_settings_path = None
        if args.settings_file:
            base_settings_path = args.settings_file
        else:
            print("Exacting initial settings from form file")
            base_settings_path = os.path.abspath("base_settings.fps")
            preform.api.scene_save_fps_file_post(formlabs.SceneSaveFpsFilePostRequest(file=base_settings_path))

        print("Loading initial settings file")
        with open(base_settings_path, 'r') as f:
            base_settings = json.load(f)

        print("Generating variations...")
        variations = generate_variations(base_settings, args)
        print(f"Generated {len(variations)} variations")

        for idx, variation in enumerate(variations):
            print(f"Running variation {idx+1}/{len(variations)}: {variation.name}")

            settings_file = f"settings_{variation.name}.fps"
            with open(settings_file, 'w') as f:
                json.dump(variation.settings, f, indent=4)

            preform.api.scene_put(formlabs.SceneTypeModel({
                "fps_file": os.path.abspath(settings_file)
            }))
            print("Estimating print time")
            estimated_print_time_s = preform.api.scene_estimate_print_time_post().total_print_time_s
            base_form_file_name_without_extension = os.path.splitext(args.form_file)[0]
            job_name = f"{base_form_file_name_without_extension}{variation.name}"
            variation_form_file_name = f"{job_name}.form"
            print(f"saving {variation_form_file_name}")
            preform.api.scene_save_form_post(formlabs.LoadFormPostRequest(file=os.path.abspath(variation_form_file_name)))

            if args.printers:
                printer_id = args.printers[idx % len(args.printers)]
                print(f"Slicing and uploading job {job_name} to printer {printer_id}...")
                preform.api.scene_print_post(formlabs.models.ScenePrintPostRequest(printer=printer_id, job_name=job_name))
                print(f"Job upload complete")

            # Record report data
            report_data.append({
                'variation_name': variation.name,
                'estimated_print_time_s': estimated_print_time_s,
                'print_time_decrease_percentage': (base_estimated_print_time_s - estimated_print_time_s) / base_estimated_print_time_s,
                'settings_file': settings_file,
                'diffs': get_settings_diff(base_settings, variation.settings)
            })

            # TODO: downselect to N variations based on a spread of print time decrease
            generate_report(report_data, args.report_file)

def parse_args():
    parser = argparse.ArgumentParser(description="3D Print Job Speed Optimization Tool")
    parser.add_argument('form_file', help='Path to starting .form file')

    parser.add_argument('--settings_file', action='store_true', help='Path to starting .fps settings file')
    parser.add_argument('--reduce_wiping', action='store_true', help='Apply reduced wiping optimization')
    parser.add_argument('--reduce_exposure', action='store_true', help='Apply reduced exposure optimization')
    parser.add_argument('--increase_layer_height', action='store_true', help='Apply increased layer height optimization')

    parser.add_argument('--printers', nargs='*', help='List of printer serial names to send jobs to')
    parser.add_argument('--report_file', default='report.md', help='Output report file')

    args = parser.parse_args()
    return args


class VariationOption:
    def __init__(self, name, func):
        self.name = name
        self.func = func

class Variation:
    def __init__(self, name, settings):
        self.name = name
        self.settings = settings


def generate_variations(base_settings, args) -> list[Variation]:
    reduce_wipe_options = [
        VariationOption("one_way_wipe", lambda settings: reduce_wiping(settings, -1)),
        VariationOption("disable_wiping", lambda settings: reduce_wiping(settings, 0)),
    ]
    reduce_expose_options = [
        VariationOption("reduce_exposure_10", lambda settings: reduce_exposure(settings, 0.1)),
        VariationOption("reduce_exposure_20", lambda settings: reduce_exposure(settings, 0.2)),
        VariationOption("reduce_exposure_30", lambda settings: reduce_exposure(settings, 0.3)),
    ]
    increase_layer_height_options = [
        VariationOption("increase_layer_height_0.11", lambda settings: increase_layer_height(settings, 0.11)),
        VariationOption("increase_layer_height_0.12", lambda settings: increase_layer_height(settings, 0.12)),
        VariationOption("increase_layer_height_0.13", lambda settings: increase_layer_height(settings, 0.13)),
        VariationOption("increase_layer_height_0.14", lambda settings: increase_layer_height(settings, 0.14)),
        VariationOption("increase_layer_height_0.15", lambda settings: increase_layer_height(settings, 0.15)),
        VariationOption("increase_layer_height_0.16", lambda settings: increase_layer_height(settings, 0.16)),
        VariationOption("increase_layer_height_0.17", lambda settings: increase_layer_height(settings, 0.17)),
    ]

    options = []
    if args.reduce_wiping:
        options.append(reduce_wipe_options)
    if args.reduce_exposure:
        options.append(reduce_expose_options)
    if args.increase_layer_height:
        options.append(increase_layer_height_options)
    
    if len(options) == 0:
        print("No options selected")
        return []

    combinations = list(itertools.product(*options))
    variations = []
    for combo in combinations:
        settings = copy.deepcopy(base_settings)
        combined_name = ""
        for variation_option in combo:
            settings = variation_option.func(settings)
            combined_name += f"_{variation_option.name}"
        settings = update_settings_with_new_id_and_name(settings, combined_name)
        variation_number = len(variations) + 1
        combined_name = f"v{variation_number}{combined_name}"
        variations.append(Variation(combined_name, settings))
    return variations

def update_settings_with_new_id_and_name(settings, combined_name):
    settings['metadata']['id'] = "{" + str(uuid.uuid4()) + "}"
    settings['metadata']['name'] = settings['metadata']['name'] + combined_name
    return settings

def get_printer_knobs_index(settings):
    form4familyPrintIndex = -1
    for i, category in enumerate(settings['public_fields']['categories']):
        if category['key'] == 'Material_Form_4_Family_Print':
            form4familyPrintIndex = i
            break
    if form4familyPrintIndex == -1:
        raise Exception("Material_Form_4_Family_Print category not found")
    return form4familyPrintIndex

def get_printer_knobs(settings):
    form4familyPrintIndex = get_printer_knobs_index(settings)
    return settings['public_fields']['categories'][form4familyPrintIndex]['values']

def get_settings_with_new_printer_knobs(settings, knobs):
    form4familyPrintIndex = get_printer_knobs_index(settings)
    settings['public_fields']['categories'][form4familyPrintIndex]['values'] = knobs
    return settings

def reduce_wiping(settings, wipe_behavior_mode_value):
    knobs = get_printer_knobs(settings)
    if 'wipe_behavior_pattern' not in knobs:
        raise Exception("wipe_behavior_pattern not found in settings")
    knobs['wipe_behavior_pattern'] = [{"wipe_behavior": wipe_behavior_mode_value}]
    return get_settings_with_new_printer_knobs(settings, knobs)

def reduce_exposure(settings, percent_decrease):
    knobs = get_printer_knobs(settings)
    
    knobs['model_fill_exposure_mJpcm2'] = round(knobs['model_fill_exposure_mJpcm2'] * (1 - percent_decrease), 1)
    for i,v in enumerate(knobs['overhang_fill_exposures']):
        knobs['overhang_fill_exposures'][i]["exposure_mJpcm2"] = round(v["exposure_mJpcm2"] * (1 - percent_decrease), 1)
    knobs['perimeter_fill_exposure_mJpcm2'] = knobs['model_fill_exposure_mJpcm2']
    knobs['supports_fill_exposure_mJpcm2'] = knobs['model_fill_exposure_mJpcm2']
    knobs['top_surface_exposure_mJpcm2'] = knobs['model_fill_exposure_mJpcm2']
    if 'irradiance_mWpcm2' not in knobs:
        raise Exception("irradiance_mWpcm2 not found in settings")
    knobs['irradiance_mWpcm2'] = 16
    if 'post_expose_cure_wait_s' not in knobs:
        raise Exception("post_expose_cure_wait_s not found in settings")
    knobs['post_expose_cure_wait_s'] = 0
    return get_settings_with_new_printer_knobs(settings, knobs)

def increase_layer_height(settings, layer_thickness_mm):
    coreSceneIndex = -1
    for i, category in enumerate(settings['public_fields']['categories']):
        if category['key'] == 'Core_Scene':
            coreSceneIndex = i
            break
    if coreSceneIndex == -1:
        raise Exception("Core_Scene category not found")
    
    knobs = settings['public_fields']['categories'][coreSceneIndex]['values']
    knobs['layer_thickness']['layer_thickness_mm'] = layer_thickness_mm
    settings['public_fields']['categories'][coreSceneIndex]['values'] = knobs
    return settings

def get_settings_diff(base_settings, new_settings):
    base_str = json.dumps(base_settings, sort_keys=True, indent=4)
    new_str = json.dumps(new_settings, sort_keys=True, indent=4)
    diff = difflib.unified_diff(base_str.splitlines(), new_str.splitlines(), lineterm='')
    return '\n'.join(diff)

def generate_report(report_data, report_file):
    with open(report_file, 'w') as f:
        for data in report_data:
            print_time_decrease_percentage = data['print_time_decrease_percentage'] * 100
            estimated_print_time_s = data['estimated_print_time_s']
            f.write(f"# Variation: {data['variation_name']} [{print_time_decrease_percentage:.1f}% print time decrease]\n")
            f.write(f"- Estimated Print Time: {estimated_print_time_s:.1f} seconds\n")
            f.write(f"- Settings File: {data['settings_file']}\n")
            f.write("- Settings Differences:\n")
            f.write("```\n")
            f.write(f"{data['diffs']}\n")
            f.write("```\n")
            f.write("\n")
    print(f"Result summary written to {report_file}")

if __name__ == '__main__':
    main()
