import logging as _logging
import sys as _sys

from . import core as _core
from . import export as _export

logger = _logging.getLogger(__name__)


def run(infile, *, output, color=True, complete_flow=False, scale=1.0):
    try:
        if infile == '-':  # the special argument '-' means stdin
            template = _core.Template.from_json(_sys.stdin)
        else:
            with open(infile) as fp:
                template = _core.Template.from_json(fp)
    except TypeError:
        logger.error('Invalid JSON input')  # noqa: TRY400 (reason: user-facing message)
        _sys.exit(1)
    except ValueError:
        logger.error('Invalid linking matrix')  # noqa: TRY400 (reason: user-facing message)
        _sys.exit(1)
    except OSError as err:
        logger.critical(f'Unable to read input: {err}')
        _sys.exit(2)

    logger.info('Input matrix')
    for row in template.matrix:
        logger.info(f'  {row}')

    logger.info('Starting creation of the SVG template')
    exporter = _export.SVGExporter()
    try:
        if output == '-':  # the special argument '-' means stdout
            exporter.write(
                template,
                output=_sys.stdout,
                color=color,
                complete_flow=complete_flow,
                scale=scale,
            )
        else:
            with open(output, mode='w') as fp:
                exporter.write(
                    template,
                    output=fp,
                    color=color,
                    complete_flow=complete_flow,
                    scale=scale,
                )
    except OSError as err:
        logger.critical(f'Unable to write output: {err}')
        _sys.exit(code=2)
    logger.info('Finished creation of the SVG template')
