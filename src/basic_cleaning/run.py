#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
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

    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(artifact_local_path)

    logger.info("Drop the outliers")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    logger.info("Drop the outliers in geolocation")
    idx1 = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx1].copy()

    logger.info("Save results")
    filename = "clean_sample.csv"
    df.to_csv(filename, index = False)

    artifact = wandb.Artifact(
      args.output_artifact,
      type=args.output_type,
      description=args.output_description)

    artifact.add_file("clean_sample.csv")

    logger.info("Logging artifact")
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")


    parser.add_argument(
        "--input_artifact",
        type= str,
        help= "The name of the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type= str,
        help= "The name of the resulted artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type= str,
        help= "Type of the artifact",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type= str,
        help= "Description of the artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type= float,
        help= "The minimum price of the artifact",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type= float,
        help= "The maximum price of the artifact",
        required=True
    )

    args = parser.parse_args()

    go(args)
