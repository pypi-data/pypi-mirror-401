import pandas as pd
import importlib.resources

datasets = {
    "adult": "Adult census income dataset.",
    "advertising": "The dataset from an organization’s social media ad campaign.",
    "bank": "Bank marketing dataset.",
    "caravan": "Caravan insurance dataset.",
    "cereal": "Cereal nutrition dataset.",
    "churn": "Credit card churn dataset.",
    "churn_ibm": "Telecom churn dataset (IBM).",
    "churn_tel": "Telecom churn dataset (MLC).",
    "corona": "COVID-19 related dataset.",
    "diamonds": "Diamonds dataset.",
    "drug": "Drug classification dataset.",
    "gapminder": "Gapminder dataset.",
    "house": "House sales dataset.",
    "house_price": "House price dataset.",
    "insurance": "Insurance dataset.",
    "marketing": "Marketing campaigns dataset.",
    "mpg": "Auto MPG dataset.",
    "red_wines": "Red wine quality dataset.",
    "risk": "Risk analysis dataset.",
    "white_wines": "White wine quality dataset.",
}


def load(name: str) -> pd.DataFrame:
    name = name.strip().lower().replace("_", "")  # remove underscores
    # Build a lookup dict: stripped keys -> canonical keys
    lookup = {k.replace("_", ""): k for k in datasets.keys()}

    if name in lookup:
        canonical_name = lookup[name]  # get the actual dataset key (with underscore)
        try:
            with (
                importlib.resources.files("dsf.data")
                .joinpath(f"{canonical_name}.pkl")
                .open("rb") as f
            ):
                return pd.read_pickle(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load dataset '{canonical_name}': {e}")
    else:
        raise ValueError(f"Dataset '{name}' does not exist.")


def dataset_table() -> str:
    """Generate a dynamic-width table of datasets."""
    name_width = max(len(name) for name in datasets) + 2
    desc_width = max(len(desc) for desc in datasets) + 2

    table_lines = [
        f"{'Dataset':<{name_width}} {'Description':<{desc_width}}",
        "-" * (name_width + desc_width),
    ]

    for name, desc in datasets.items():
        table_lines.append(f"{name:<{name_width}} {desc:<{desc_width}}")

    return "\n".join(table_lines)
