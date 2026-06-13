# formalization-flow

A plasTeX plugin for writing structured LaTeX theorems that compile to sorry-filled Lean 4 skeletons

## Requirements

<!-- List software requirements here, e.g.:
- Magma v2.29-1 or higher
- SageMath X.Y
- Python 3.x
- GNU parallel
-->

## Project layout

| Directory | Contents |
|-----------|----------|
| `computations/` | Magma `.m` and SageMath `.sage` scripts run by `verify_all.sh` |
| `logs/` | Output from `verify_all.sh` (committed as a record of the computations) |
| `src/` | Library/source code shared across computations |
| `tests/` | Test scripts |

## Running computations

To run all scripts in `computations/` in parallel (requires GNU parallel):

```bash
make verify           # uses 10 parallel jobs by default
bash verify_all.sh 4  # or call the script directly to set the job count
```

Output lands in `logs/<script-name>.txt`. SageMath scripts also produce `logs/<script-name>.timing.txt`.

## Running tests

```bash
make test
```

## Running on a remote machine

```bash
make verify_remote ssh="user@hostname"  # sync and run all computations
make copy_logs     ssh="user@hostname"  # fetch logs back afterwards
```

## Troubleshooting

**`parallel: command not found`**

GNU parallel is not installed.  Install it with:

```bash
# macOS
brew install parallel

# Debian / Ubuntu
sudo apt install parallel

# RHEL / Fedora
sudo dnf install parallel
```
