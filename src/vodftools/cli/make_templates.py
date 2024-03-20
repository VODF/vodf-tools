"""
Writes out the VODF model(s) in FITS template (.tpl) format
"""

from argparse import ArgumentParser, FileType


from ..fits_template import write_fits_template, fits_template
from ..models.level1 import event_file
from ..version import __version__

parser = ArgumentParser("vodf-make-templates", description=__doc__)
parser.add_argument(
    "-o", "--output", type=str, help="output file. If not specified, use STDOUT"
)
parser.add_argument("--version", action="version", version=__version__)


def main():
    args = parser.parse_args()

    if args.output:
        write_fits_template(event_file, args.output)

    else:
        for line in fits_template(event_file):
            print(line)


if __name__ == "__main__":
    main()
