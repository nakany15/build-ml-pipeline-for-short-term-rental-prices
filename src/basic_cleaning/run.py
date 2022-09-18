#!/usr/bin/env python
"""
An example of a step using MLflow and Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    local_path = wandb.use_artifact(args.input_artifact).file()
    logger.info(f'loading {local_path}')
    df = pd.read_csv(local_path)
    logger.debug(df.shape)
    # Drop outliers
    min_price = args.min_price
    max_price = args.max_price
    logger.info(f'exclude outliers of price.')
    logger.debug(f'min:{min_price}')
    logger.debug(f'max:{max_price}')
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    logger.info('export clean_sample.csv to local')
    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    logger.info('export clean_sample.csv to W&B as an artifact')
    run.log_artifact(artifact)
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "input_artifact", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help='input data name',## INSERT DESCRIPTION HERE,
    )

    parser.add_argument(
        "output_artifact", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help='output artifact name',## INSERT DESCRIPTION HERE,
    )

    parser.add_argument(
        "output_type", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help='output file type',## INSERT DESCRIPTION HERE,
    )

    parser.add_argument(
        "output_description", 
        type=str,## INSERT TYPE HERE: str, float or int,
        help='output data file description',## INSERT DESCRIPTION HERE,
    )

    parser.add_argument(
        "min_price", 
        type=float,## INSERT TYPE HERE: str, float or int,
        help='minimum price threshold to truncate price',## INSERT DESCRIPTION HERE,
    )

    parser.add_argument(
        "max_price", 
        type=float,## INSERT TYPE HERE: str, float or int,
        help='maximum price threshold to truncate price',## INSERT DESCRIPTION HERE,
    )

    args = parser.parse_args()

    go(args)
