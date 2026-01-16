# instacart-order-history-download

instacart-order-history-download is a command-line tool for downloading your Instacart order history.

## Install

```bash
brew tap mike-vincent/instacart-order-history-download
brew install instacart-order-history-download
```

## Get your session cookie

Log into instacart.com, open DevTools → Cookies, and copy `_instacart_session_id`.

## Usage

```bash
instacart-order-history-download --instacart-session-id "YOUR_SESSION_ID"
instacart-order-history-download --instacart-session-id "YOUR_SESSION_ID" -n 10 -f csv -o orders.csv
```

## Options

```
--instacart-session-id   Your _instacart_session_id cookie (required)
-n, --orders             Number of orders to fetch (default: all)
-f, --format             csv, json, markdown, tsv, or yaml
-o, --output             Output filename
-q, --quiet              Quiet mode
-h, --help               Show help
```

## Output

JSON, CSV, or text with order dates, totals, retailers, and full item details.

## Author

[Mike Vincent](https://www.mikevincent.dev), Los Angeles, Calif.

## Disclaimer

Not affiliated with Maplebear Inc. d/b/a Instacart.

## Contributing

Issues and pull requests welcome.

## License

[GPL-3.0](LICENSE)
