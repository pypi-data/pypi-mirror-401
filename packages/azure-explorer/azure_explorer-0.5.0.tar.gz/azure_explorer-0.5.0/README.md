# 🔎 Azure Explorer

The purpose of this package is to provide a simple interface for exploring resources in your Azure Cloud environment. The package consists of a CLI tool and a Python library.

---

## Setup

Install the latest version of Azure Explorer with

```console
pip install azure-explorer
```

---

## Usage

### CLI tool

The CLI tool provides a way of navigating your Azure Cloud resources in the command line. Run the CLI tool with

```console
ax
```

![cli-tool](docs/cli-tool.png)

### Python library

The Python library provides a way of interacting with our Azure Cloud resources in in Python code. Use the Python library with

```python
>>> import azure_explorer as ax
>>> tenant = ax.get_tenant_manager()
>>> tenant.list_subscription_names()
[
    'development-subscription',
    'preproduction-subscription',
    'production-subscription',
    'test-subscription',
]

>>> container = ax.get_container_manager(
    storage_account_name='sadataprod',
    container_name='documents',
)
>>> container.list_dir()
[
    'dir1',
    'dir2',
    'file1.txt',
    'file2.jpg',
    'file3.pdf',
]
```