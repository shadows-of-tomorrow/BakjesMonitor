import argparse
from brain.gui import GUI
from brain.engine import Engine


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--mode', action='store', type=str, required=True)
    args = arg_parser.parse_args()
    run_mode = args.mode.lower()
    return run_mode


def main():
    run_mode = parse_args()
    if run_mode == 'gui':
        GUI(engine=Engine()).run()
    elif run_mode == 'engine':
        Engine().run()
    else:
        raise Exception(f"Run mode {run_mode} not recognized!")


if __name__ == "__main__":
    main()
