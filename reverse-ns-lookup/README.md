# Reverse NS Lookup

This set of scripts allows you to perform a **reverse nameserver lookup**, collect the hostnames associated with a nameserver, merge results, convert them to CSV, and find common hostnames across multiple nameservers.


## 1. Pulling Data from SecurityTrails

1. Identify the nameserver you want to query, e.g., `etienne.ns.cloudflare.com`. The `QUERY_NAMESERVER` variable has to be updated to this value.

2. Open the URL for that nameserver in SecurityTrails (replace the page number accordingly):

   ```
   https://securitytrails.com/list/ns/etienne.ns.cloudflare.com?page=2
   ```

3. Open the **Developer Tools → Network tab**, then click to navigate to another page in the list.

4. Find the request that retrieves the JSON data. Copy the following values from the request details and update the `1-pull.py` script:

   * `URL`: The exact request URL
   * `User-Agent`: Your browser's user agent
   * `Cookie`: Session cookie from the request

5. Update the `END_PAGE` variable with the number of the last page.

Some values has already been filled up in the "CONFIGURATION" section of `1-pull.py`. Just update the other values accordingly. Make you update both the cookie and the user agent for it to work. Otherwise, you might get 403s. Use your common sense to update the other values too.

## 2. Merging JSON Files

After collecting data using `1-pull.py`, merge all page files into a single JSON file:

```bash
python 2-merge.py etienne.ns.cloudflare.com
```

* This creates a single file: `etienne.ns.cloudflare.com.json`
* By default, the script moves the individual page JSON files into a folder named after the nameserver.
* Optionally, you can delete the individual files with `-d` instead of moving them.

## 3. Converting JSON to CSV

Once merged, you can convert the JSON file to CSV for easier analysis:

```bash
python 3-to-csv.py etienne.ns.cloudflare.com.json
```

* The CSV will have `hostname` as the first column.
* List fields like `host_provider` and `mail_provider` are joined using `|`.
* You can specify a custom delimiter with the `-d` option.

## 4. Finding Common Hostnames Across Multiple Nameservers

If you repeated the above steps for another nameserver (e.g., `daisy.ns.cloudflare.com`), you can find hostnames that use **both nameservers**:

```bash
python 4-find-common.py daisy.ns.cloudflare.com.json etienne.ns.cloudflare.com.json
```

* The script outputs a file named `common-YYYY-MM-DD.json`
* The JSON includes the following keys:

```json
{
  "ns": "daisy.ns.cloudflare.com",
  "date": "2026-01-18",
  "total_records": 1000,
  "records": [
    ...
  ]
}
```

* You can pass as many JSON files as arguments to find hostnames common across multiple nameservers.
