# vcf-stats-viz

`vcf-stats-viz` is a command-line tool for efficient analysis of VCF (Variant Call Format) files and for generating an interactive local web dashboard for variant exploration.

The package is designed to handle large-scale VCF files with a strong emphasis on low memory usage. It achieves this through chunk-based processing, avoiding loading the entire file into memory. Analysis results are stored on disk and can be reused without reprocessing the original VCF file.

## Key features

- Memory-efficient processing of large VCF files using chunk-based parsing
- Generation of variant statistics and summary datasets
- Persistent storage of analysis results and metadata
- Local web-based dashboard for interactive visualization and filtering of variants
- Support for multiple stored analyses
- Simple and reproducible command-line interface

## Installation

```bash
pip install vcf-stats-viz
```

The package installs the following command-line entry point:

```bash
vcf-analyze
```

## Basic usage

Run a complete analysis of a VCF file and launch the local web dashboard:

```bash
vcf-analyze input.vcf
```

By default, the dashboard is available at:

```
http://127.0.0.1:5000
```

## Common options

Limit the number of processed variants:

```bash
vcf-analyze input.vcf 100000
```

Adjust the chunk size used during processing:

```bash
vcf-analyze input.vcf --chunk-size 50000
```

Run the analysis without launching the web dashboard:

```bash
vcf-analyze input.vcf --no-dashboard
```

Launch the web dashboard using previously generated results:

```bash
vcf-analyze --dashboard-only
```

## Use cases

- Exploratory analysis of genomic variants
- Preliminary processing of large VCF datasets
- Local visualization of variant statistics without external services
- Validation and debugging of bioinformatics pipelines

## Console entry point

The package exposes the following console script:

```toml
vcf-analyze = "vcf_stats.main:main"
```

## License

This project is licensed under the MIT License.
