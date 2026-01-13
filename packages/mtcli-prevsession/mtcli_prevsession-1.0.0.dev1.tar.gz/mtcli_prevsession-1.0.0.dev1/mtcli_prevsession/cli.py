"""
Comando mtcli: prevsession
"""

import click

from .conf import SYMBOL
from .controller import PrevSessionController
from .view import PrevSessionTextView


@click.command()
@click.version_option(package_name="mtcli-prevsession")
@click.option(
    "--symbol",
    "-s",
    default=SYMBOL,
    show_default=True,
    help="Ativo negociado no MT5.",
)
def prevsession(symbol: str):
    """
    Exibe preços do pregão anterior e níveis percentuais
    baseados no preço de ajuste.
    """
    controller = PrevSessionController(symbol)
    view = PrevSessionTextView()

    prices, variations = controller.run()
    view.render(symbol, prices, variations)
