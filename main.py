from decimal import Decimal

import click
from scaler import AdventureBundle


@click.command()
@click.argument('input_adventure_file', type=click.File("rb"))
@click.argument('output_adventure_file', type=click.Path(resolve_path=True))
@click.argument('scale_ratio', type=click.FloatRange(min=0.1, max=10))
def scale_adventure(input_adventure_file, output_adventure_file, scale_ratio):
    """Simple program that rescales all scenes in a foundry Adventure Exporter/Importer .fvttadv file"""
    adventure_bundle = AdventureBundle()
    adventure_bundle.perform_scaling(
        input_file=input_adventure_file,
        output_file=output_adventure_file,
        scale=Decimal(scale_ratio)
    )


if __name__ == '__main__':
    scale_adventure()
