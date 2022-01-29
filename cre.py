import argparse
import os
import sys
import unittest
from typing import List

import click  # type: ignore
import coverage  # type: ignore
from flask_migrate import Migrate  # type: ignore

from application import create_app, sqla  # type: ignore
from application.cmd import cre_main

# Hacky solutions to make this both a command line application with argparse and a flask application

app = create_app(mode=os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, sqla, render_as_batch=True)

# flask <x> commands


@app.cli.command()  # type: ignore
@click.option(
    "--cover/--no-cover", default=False, help="Run tests under code coverage."
)  # type: ignore
@click.argument("test_names", nargs=-1)  # type: ignore
def test(cover: coverage.Coverage, test_names: List[str]) -> None:
    COV = None
    if cover or os.environ.get("FLASK_COVERAGE"):
        COV = coverage.coverage(
            branch=True,
            include="application/*",
            check_preimported=True,
            config_file="application/tests/.coveragerc",
        )
        COV.start()

    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover("application/tests", pattern="*_test.py")
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "tmp/coverage")
        COV.html_report(directory=covdir)
        print("HTML version: file://%s/index.html" % covdir)
        COV.erase()


# python cre.py --<x> commands


def main() -> None:

    app_context = app.app_context()
    app_context.push()

    script_path = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(
        description="Add documents describing standards to a database"
    )
    parser.add_argument(
        "--add",
        action="store_true",
        help="will treat the incoming spreadsheet as a reviewed cre and add to the database",
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="will treat the incoming spreadsheet as a new mapping, will try to map the incoming connections to existing cre\
            and will create a new spreadsheet with the result for review. Nothing will be added to the database at this point",
    )
    parser.add_argument(
        "--email",
        help="used in conjuctions with --review, what email to share the resulting spreadsheet with",
        default="standards_cache.sqlite",
    )
    parser.add_argument(
        "--from_spreadsheet", help="import from a spreadsheet to yaml and then database"
    )
    parser.add_argument(
        "--print_graph",
        help="will show the graph of the relationships between standards",
    )
    parser.add_argument(
        "--cache_file",
        help="where to read/store data",
        default=os.path.join(script_path, "standards_cache.sqlite"),
    )
    parser.add_argument(
        "--cre_loc",
        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "./cres/"),
        help="define location of local cre files for review/add",
    )

    parser.add_argument(
        "--owasp_proj_meta",
        default=None,
        # default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "./cres/owasp/projects.yaml"),
        help="define location of owasp project metadata",
    )
    parser.add_argument(
        "--osib_in",
        default=None,
        help="define location of local osib file for review/add",
    )
    parser.add_argument(
        "--osib_out",
        default=None,
        help="define location of local directory to export database in OSIB format to",
    )

    parser.add_argument("--zap_in",action="store_true", help="import zap alerts by cloning zap's website and parsing the alert .md files")
    args = parser.parse_args()
    cre_main.run(args)


if __name__ == "__main__":  # if we're called directly
    main()
