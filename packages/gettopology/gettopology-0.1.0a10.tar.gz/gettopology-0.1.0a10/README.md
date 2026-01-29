# GetTopology

> **⚠️ Alpha Release** - This is an alpha version. Features may change and bugs may exist.

CLI tool for generating Azure VNet topology diagrams with enhanced features.

## What's Supported

This tool supports **Azure Virtual Networks (VNets)** only. The following Azure networking services are **not** currently supported:

- ❌ **Azure Virtual Network Manager (AVNM)** - Not supported
- ❌ **Azure Virtual WAN (VWAN)** - Not supported

The tool focuses on traditional VNet-to-VNet peering topologies, including:
- ✅ Hub and spoke VNet architectures
- ✅ VNet peering connections
- ✅ Hybrid connectivity (VPN and ExpressRoute connections)
- ✅ Network resources within VNets (subnets, route tables, NSGs, etc.)

## Installation

```bash
pip install gettopology
```

```bash
# for CLoud shell
pip install gettopology --user 
```

For the specific  alpha version:
```bash
pip install gettopology==0.1.0a3
```


## Requirements

- Python 3.10 or higher
- Azure subscription with appropriate permissions
- Azure CLI installed and configured (or Service Principal credentials)
- **For Markmap diagrams**: Node.js and npm installed
  - **After installing Node.js/npm**, install markmap CLI:
    - Regular environments:  `npm install -g markmap-cli`
  - **Azure Cloud Shell**:
      ```node
        npm install markmap-cli
      ```
          
  - Required only when using the `-vnet` flag to generate interactive VNet markmap visualizations

**Internet Access Requirements:**
- **Draw.io files (`.drawio`)**: Can be opened **offline** in Draw.io desktop app or VS Code extension
- **Index.html dashboard**: Requires internet access to load the Draw.io viewer JavaScript (CDN)
- **Markmap HTML files**: Require internet access for CDN resources (d3.js, markmap libraries) 

## Usage

After installation, use the `gettopology` command:

```bash
# Get topology for all VNets in all accessible subscriptions
gettopology

# Get topology for specific subscriptions [optional]
gettopology -s "subscription-id-1,subscription-id-2"

# Get topology from subscriptions listed in a file on new line[optional]
gettopology -f subscriptions.txt

# Specify output directory for diagrams [optional]
# If not specified, creates a timestamped directory: topology_YYYYMMDD_HHMMSS
gettopology -s "sub-id" -o ./diagrams

# Generate markmap HTML visualizations for each VNet (requires markmap-cli)
gettopology -vnet
```

### Command Line Arguments

- `-s, --subscriptions`: Comma-separated subscription IDs (optional)
- `-f, --subscriptions-file`: Path to file containing subscription IDs, one per line (optional)
- `-vnet, --virtual-network`: Generate interactive markmap HTML visualizations for each VNet (requires `markmap-cli` to be installed)
- `-o, --output`: Output directory for generated diagrams (default: creates timestamped directory `topology_YYYYMMDD_HHMMSS`)
- `--log-level`: Logging level - DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)
- `--skip-roles`: Skip role verification. By default, the tool verifies that the authenticated user/service principal has at least 'Reader' role on subscriptions before proceeding (optional)
- `--version`: Display version information

### Authentication

The tool supports multiple authentication methods, tried in this order:

1. **Azure CLI** (first): Uses `az login` credentials - tried first if available
2. **Service Principal** (second): Provide via CLI arguments, environment variables, or `.env` file
3. **Managed Identity** (third): Automatically used when running in Azure (e.g., Azure VM, App Service, Functions)


For Service Principal authentication:
```bash
gettopology --client-id "your-client-id" \
  --client-secret "your-secret" \
  --tenant-id "your-tenant-id"
```

Or use environment variables:
```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-secret"
export AZURE_TENANT_ID="your-tenant-id"
gettopology
```

Or create a `.env` file in your project directory:
```bash
# .env file
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-secret
AZURE_TENANT_ID=your-tenant-id
```

**Priority order for Service Principal credentials:**
1. CLI arguments (`--client-id`, `--client-secret`, `--tenant-id`)
2. Environment variables (`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`)
3. `.env` file (in current directory or project root)

## Output

The tool generates organized output in a timestamped directory (or specified output directory) with the following structure:

```
output_dir/
├── hld/
│   └── topology-hld.drawio    # High-Level Diagram (always generated)
├── vnet/
│   ├── vnet1-markmap.html      # Interactive markmap for each VNet (if -vnet flag used)
│   ├── vnet2-markmap.html
│   └── ...
└── index.html                  # Interactive dashboard (always generated)
```

**Note:** A zip file (`output_dir.zip`) is automatically created in the parent directory, containing all generated files. This makes it easy to download and share the complete topology visualization package.

### High-Level Diagram (HLD)

The Draw.io (`.drawio`) format diagram can be opened in:
- [Draw.io](https://app.diagrams.net/) (web)
- [diagrams.net](https://www.diagrams.net/) (desktop)
- Visual Studio Code (with Draw.io extension)

Diagrams include:
- Hub and spoke VNets with visual distinction
- Peering connections with color-coded lines
- Subnet details within VNet boxes (including all address prefixes)
- External VNets (cross-subscription/tenant peerings)
- Separate pages for hubless spokes and orphan VNets
- Separate page for hybrid connetivity (vpn and Expressroute)
- Azure Firewall , Expressoute and VPN Gateway Check(apart from subnet) are checked before putting the icons on subnet. Bastion Icon based on Subnet only.
- NSG and Route tabel icons on Subnet
- DDoS Protection and Private Endpoint icons where applicable
- Markmap for Vnets showing Subnets, peerings and routes etc.

### Markmap Visualizations (Optional)

When using the `-vnet` flag, the tool additionally generates:
- **Interactive HTML markmaps** for each VNet showing:
  - VNet details (address space, location, subscription)
  - Subnet information (name, address prefixes, route tables)
  - Route table routes (if accessible)
  - Network security groups
  - Connected resources (NAT Gateways, Private Endpoints, etc.)
- These markmap files are placed in the `vnet/` subdirectory and linked from `index.html`

**Note:** Markmap generation requires `markmap-cli` to be installed globally:
```bash
npm install -g markmap-cli
```

## Development

This project uses several code quality tools:

- **Ruff**: Fast Python linter and formatter
- **mypy**: Static type checker
- **Bandit**: Security vulnerability scanner
- **pytest**: Testing framework

To install development dependencies:
```bash
# Using uv (installs from [dependency-groups])
uv sync --group dev

# Or install in editable mode with dev dependencies
uv pip install -e ".[dev]"
```

Run code quality checks:
```bash
# Linting
uv run ruff check src/

# Type checking
uv run mypy src/

# Security scanning
uv run bandit -r src/ -c pyproject.toml

# Tests will be added on later version
uv run pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

