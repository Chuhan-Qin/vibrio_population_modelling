import subprocess
import time
import os

def run_ncbi_datasets_summary(organism, source_db, out_dir):
    # Use NCBI datasets CLI to download genomes metadata
    # The library is locally available at 'ncbi_datasets' conda environment

    # Start running
    start_time = time.time()

    # Get a summary of metadata for genomes of a given organism
    command = (f'conda run -n ncbi_datasets '+\
               f'datasets summary genome taxon \"{organism}\" --assembly-source {source_db}')

    process = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True)

    # Write the output and write the error message to a log file
    stdout = process.stdout
    stderr = process.stderr

    if stdout:
        with open(f'{out_dir}/genome_summary.txt', 'w') as out_txt:
            out_txt.write(stdout)

    if stderr:
        with open(f'{out_dir}/error_log.txt', 'w') as log_file:
            log_file.write(stderr)

    # Print the time taken to run the command
    end_time = time.time()
    print(f'Total execution time: {end_time - start_time} seconds')


def run_ncbi_datasets_download(organism, source_db, out_dir, filename):
    # Use NCBI datasets CLI to download genomes sequences
    # The library is locally available at 'ncbi_datasets' conda environment

    # Start running
    start_time = time.time()

    # Download genomes of a given organism
    command = (f'conda run -n ncbi_datasets '+\
               f'datasets download genome taxon \"{organism}\" --assembly-source {source_db} '+\
               f'--include genome --filename {out_dir}/{filename}')

    process = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True)

    # Write the output and write the error message to a log file
    stdout = process.stdout
    stderr = process.stderr

    if not os.path.exists(f'{out_dir}/data'):
        os.mkdir(f'{out_dir}/data')

    if stdout:
        with open(f'{out_dir}/data/download_log.txt', 'w') as out_txt:
            out_txt.write(stdout)

    if stderr:
        with open(f'{out_dir}/data/error_log.txt', 'w') as log_file:
            log_file.write(stderr)

    # Print the time taken to run the command
    end_time = time.time()
    print(f'Total execution time: {end_time - start_time} seconds')
