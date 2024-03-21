"""Writes out the VODF model(s) in FITS template (.tpl) format."""

from argparse import ArgumentParser

from vodftools import __version__
from vodftools.fits_template import fits_template, write_fits_template
from vodftools.models.level1 import event_file, irf_file

parser = ArgumentParser("vodf-make-templates", description=__doc__)
parser.add_argument(
    "-o", "--output", type=str, help="output file. If not specified, use STDOUT"
)
parser.add_argument("--version", action="version", version=__version__)


def main():
    """Generate templates."""
    args = parser.parse_args()

    for schema in [event_file, irf_file]:
        if args.output:
            write_fits_template(schema, args.output)
        else:
            for line in fits_template(schema):
                print(line)


if __name__ == "__main__":
    main()
