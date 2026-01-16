#!/usr/bin/env python3
"""
Instacart order history exporter.

Exports your Instacart orders with full item details to JSON, CSV, or text.
No external dependencies - uses only Python stdlib.
"""

import argparse
import csv
import json
import sys
import time
import urllib.request
import urllib.error


def fetch_orders(session_id, max_orders=None, max_pages=100, verbose=True):
    """Fetch orders from Instacart API."""

    headers = {
        'Host': 'www.instacart.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Client-Identifier': 'web',
        'Cookie': f'_instacart_session_id={session_id}',
    }

    all_orders = []
    page = 1

    while page <= max_pages:
        if verbose:
            print(f'Fetching page {page}...', file=sys.stderr)

        url = f'https://www.instacart.com/v3/orders?page={page}'

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))

            orders = data.get('orders', [])

            if not orders:
                if verbose:
                    print('No more orders.', file=sys.stderr)
                break

            for order in orders:
                order_data = extract_order(order)
                all_orders.append(order_data)

                if max_orders and len(all_orders) >= max_orders:
                    if verbose:
                        print(f'Reached {max_orders} orders.', file=sys.stderr)
                    return all_orders

            if verbose:
                items = sum(len(d['items']) for o in all_orders for d in o['deliveries'])
                print(f'  {len(all_orders)} orders, {items} items so far', file=sys.stderr)

            meta = data.get('meta', {}).get('pagination', {})
            if meta.get('next_page') is None:
                if verbose:
                    print('Reached last page.', file=sys.stderr)
                break

            page += 1
            time.sleep(0.5)

        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry = int(e.headers.get('Retry-After', 60))
                if verbose:
                    print(f'Rate limited. Waiting {retry}s...', file=sys.stderr)
                time.sleep(retry)
                continue
            elif e.code == 401:
                print('Error: Invalid or expired session. Get a fresh cookie.', file=sys.stderr)
                break
            else:
                print(f'Error: HTTP {e.code}', file=sys.stderr)
                break
        except Exception as e:
            print(f'Error: {e}', file=sys.stderr)
            break

    return all_orders


def extract_order(order):
    """Extract relevant fields from API order response."""
    total_str = order.get('total', '$0')
    try:
        total = float(total_str.replace('$', '').replace(',', ''))
    except:
        total = None

    order_data = {
        'id': order.get('id'),
        'status': order.get('status'),
        'total': total,
        'total_display': order.get('total'),
        'created_at': order.get('created_at'),
        'deliveries': []
    }

    for delivery in order.get('order_deliveries', []):
        delivery_data = {
            'retailer': delivery.get('retailer', {}).get('name'),
            'delivered_at': delivery.get('delivered_at'),
            'items': []
        }

        for order_item in delivery.get('order_items', []):
            item = order_item.get('item', {})
            delivery_data['items'].append({
                'name': item.get('name'),
                'quantity': order_item.get('qty'),
                'size': item.get('size'),
                'product_id': item.get('product_id'),
            })

        order_data['deliveries'].append(delivery_data)

    return order_data


def output_json(orders, file=sys.stdout):
    json.dump(orders, file, indent=2)
    file.write('\n')


def output_csv(orders, file=sys.stdout):
    writer = csv.writer(file)
    writer.writerow(['order_id', 'order_date', 'order_total', 'retailer',
                     'item_name', 'quantity', 'size', 'product_id'])

    for order in orders:
        for delivery in order['deliveries']:
            for item in delivery['items']:
                writer.writerow([
                    order['id'],
                    order['created_at'],
                    order['total'],
                    delivery['retailer'],
                    item['name'],
                    item['quantity'],
                    item['size'],
                    item['product_id'],
                ])


def output_tsv(orders, file=sys.stdout):
    file.write('order_id\torder_date\torder_total\tretailer\titem_name\tquantity\tsize\tproduct_id\n')
    for order in orders:
        for delivery in order['deliveries']:
            for item in delivery['items']:
                row = [
                    str(order['id'] or ''),
                    str(order['created_at'] or ''),
                    str(order['total'] or ''),
                    str(delivery['retailer'] or ''),
                    str(item['name'] or ''),
                    str(item['quantity'] or ''),
                    str(item['size'] or ''),
                    str(item['product_id'] or ''),
                ]
                file.write('\t'.join(row) + '\n')


def output_markdown(orders, file=sys.stdout):
    file.write('| order_id | order_date | order_total | retailer | item_name | quantity | size | product_id |\n')
    file.write('|----------|------------|-------------|----------|-----------|----------|------|------------|\n')
    for order in orders:
        for delivery in order['deliveries']:
            for item in delivery['items']:
                file.write(f"| {order['id']} | {order['created_at']} | {order['total']} | {delivery['retailer']} | {item['name']} | {item['quantity']} | {item['size'] or ''} | {item['product_id']} |\n")


def output_yaml(orders, file=sys.stdout):
    for order in orders:
        file.write(f"- id: {order['id']}\n")
        file.write(f"  status: {order['status']}\n")
        file.write(f"  total: {order['total']}\n")
        file.write(f"  created_at: \"{order['created_at']}\"\n")
        file.write(f"  deliveries:\n")
        for delivery in order['deliveries']:
            file.write(f"    - retailer: \"{delivery['retailer']}\"\n")
            file.write(f"      delivered_at: \"{delivery['delivered_at']}\"\n")
            file.write(f"      items:\n")
            for item in delivery['items']:
                name = str(item['name'] or '').replace('"', '\\"')
                size = str(item['size'] or '').replace('"', '\\"')
                file.write(f"        - name: \"{name}\"\n")
                file.write(f"          quantity: {item['quantity']}\n")
                file.write(f"          size: \"{size}\"\n")
                file.write(f"          product_id: {item['product_id']}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Export Instacart order history.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
To get your session cookie:
  Log into instacart.com, open DevTools → Cookies, copy _instacart_session_id
''')

    parser.add_argument('--instacart-session-id', '-instacart-session-id', required=True,
                        help='Your _instacart_session_id cookie value')

    parser.add_argument('--orders', '-n', type=int, help='Number of orders to fetch (default: all)')

    parser.add_argument('--format', '-f', choices=['csv', 'json', 'markdown', 'tsv', 'yaml'],
                        default='json', help='Output format (default: json)')
    parser.add_argument('--output', '-o', type=str, help='Output filename')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode')

    args = parser.parse_args()

    orders = fetch_orders(args.instacart_session_id, max_orders=args.orders, verbose=not args.quiet)

    if not orders:
        print('No orders found.', file=sys.stderr)
        sys.exit(1)

    output_file = open(args.output, 'w') if args.output else sys.stdout

    try:
        if args.format == 'json':
            output_json(orders, output_file)
        elif args.format == 'csv':
            output_csv(orders, output_file)
        elif args.format == 'tsv':
            output_tsv(orders, output_file)
        elif args.format == 'markdown':
            output_markdown(orders, output_file)
        elif args.format == 'yaml':
            output_yaml(orders, output_file)
    finally:
        if args.output:
            output_file.close()

    if not args.quiet:
        total = sum(o['total'] or 0 for o in orders)
        items = sum(len(d['items']) for o in orders for d in o['deliveries'])
        print(f'\nExported {len(orders)} orders ({items} items, ${total:,.2f})', file=sys.stderr)


if __name__ == '__main__':
    main()
