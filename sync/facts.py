facts = {
    "src": "G:/Mi unidad",
    "tgt": "Z:/FLOWER",
    "CH_ASSETS_FOLDER": "210_ASSETS_CH",
    "CH_FOLDER_RE": r"CH_(?P<name>[a-zA-Z][a-zA-Z0-9]+)",
    "CH_FILE_RE": (
        r"(?P<name>[a-zA-Z][a-zA-Z0-9]+)_v(?P<version>[0-9]{2})"
        r".*?\.ma"
    ),
    "CH_FOLDER_TPL": "CH_{name}",
    "CH_FILE_TPL": "{name}_v{version:0>2}.ma"
}
