# OpenData Research Tools

A lightweight Python library for searching biomedical databases and returning standardized data.

## Philosophy

**Focus on search, not management:**
- ✅ Search multiple open biomedical databases
- ✅ Return standardized Python dictionaries
- ✅ Optional HTTP caching for performance
- ❌ No data management or storage
- ❌ No opinionated workflows
- ❌ Minimal dependencies (only `requests`)

Let your application decide how to store, process, and manage the data.

## Features

- **10+ Data Sources**: PubMed, NCBI Gene, UniProt, ChEMBL, PubChem, Protein Structures, WikiData, Clinical Trials, and more
- **Standardized Output**: All tools return consistent dictionary formats
- **HTTP Caching**: Optional caching to reduce API calls and improve performance
- **Gene Resolution**: Resolve gene symbols across multiple databases
- **Zero Configuration**: Works out of the box with sensible defaults
- **Lightweight**: Only one dependency (`requests`)

## Installation

```bash
pip install opendata-research-tools
```

## Quick Start

### Basic Search

```python
from opendata_research_tools.search import PubMedSearchTool

# Create a search tool instance
tool = PubMedSearchTool(enable_cache=True)

# Search PubMed
results = tool.search(query="cancer immunotherapy", max_results=10)

# Results is a list of dictionaries
for article in results:
    print(f"Title: {article['title']}")
    print(f"PMID: {article['pmid']}")
    print(f"Authors: {article['authors']}")
    print(f"Year: {article['year']}")
    print()
```

### Multiple Data Sources

```python
from opendata_research_tools.search import (
    PubMedSearchTool,
    NCBIGeneSearchTool,
    UniProtSearchTool,
    ChEMBLSearchTool
)

# Search literature
pubmed = PubMedSearchTool()
articles = pubmed.search("JAK2 V617F")

# Search gene databases
gene_tool = NCBIGeneSearchTool()
gene_info = gene_tool.search("JAK2")

# Search protein databases
uniprot = UniProtSearchTool()
protein_info = uniprot.search("JAK2")

# Search for compounds
chembl = ChEMBLSearchTool()
compounds = chembl.search(target="JAK2", activity_type="inhibitor")

# All results are dictionaries - use them however you want!
# Save to database, process with pandas, generate reports, etc.
```

### Custom Caching

```python
from opendata_research_tools.search import PubMedSearchTool

# Disable caching
tool = PubMedSearchTool(enable_cache=False)

# Custom cache directory
tool = PubMedSearchTool(enable_cache=True, cache_dir="./my_cache")
```

## Supported Databases

| Database | Tool | Description |
|----------|------|-------------|
| PubMed | `PubMedSearchTool` | Scientific literature and research papers |
| NCBI Gene | `NCBIGeneSearchTool` | Gene information, sequences, and annotations |
| UniProt | `UniProtSearchTool` | Protein sequences, functions, and structures |
| ChEMBL | `ChEMBLSearchTool` | Bioactive molecules and drug-like compounds |
| PubChem | `PubChemSearchTool` | Chemical compounds and their properties |
| Protein Structures | `ProteinStructureSearchTool` | PDB and AlphaFold protein structures |
| WikiData | `WikiDataSearchTool` | Structured knowledge graph data |
| Clinical Trials | `ClinicalTrialsSearchTool` | Clinical trial information |
| News | `NewsSearchTool` | Industry news and developments |
| Patents | `PatentSearchTool` | Patent information |

## Return Format

Each tool returns a list of dictionaries with standardized fields. Example for PubMed:

```python
[
    {
        'pmid': '12345678',
        'title': 'Article Title',
        'authors': 'Smith J, Doe J',
        'journal': 'Nature',
        'year': '2023',
        'abstract': 'Article abstract text...',
        'keywords': ['cancer', 'therapy'],
        'doi': '10.1234/example',
        'url': 'https://pubmed.ncbi.nlm.nih.gov/12345678/'
    },
    ...
]
```

See the [API Reference](docs/api_reference.md) for detailed field descriptions for each data source.

## Gene Symbol Resolution

Resolve gene symbols across multiple databases:

```python
from opendata_research_tools.utils import GeneSynonymResolver

resolver = GeneSynonymResolver()
result = resolver.resolve("TP53")

print(f"Canonical Symbol: {result.canonical_symbol}")
print(f"Entrez ID: {result.entrez_id}")
print(f"Aliases: {result.aliases}")
print(f"Organism: {result.organism}")
```

## Documentation

- [Quick Start Guide](docs/quickstart.md)
- [API Reference](docs/api_reference.md)
- [Examples](examples/)

## Development

```bash
# Clone the repository
git clone https://github.com/xxxxx/opendata-research-tools.git
cd opendata-research-tools

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=opendata_research_tools --cov-report=html
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Citation

- Documentation: https://opendata-research-tools.readthedocs.io
