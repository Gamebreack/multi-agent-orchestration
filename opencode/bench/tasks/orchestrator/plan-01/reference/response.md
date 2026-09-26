```json
{
  "tasks": [
    {
      "id": "t1",
      "files": ["inventory/models.py"],
      "depends_on": [],
      "summary": "Add Item.is_low_stock(threshold)"
    },
    {
      "id": "t2",
      "files": ["inventory/report.py"],
      "depends_on": ["t1"],
      "summary": "Add low_stock(items, threshold) and format_alert(items)"
    },
    {
      "id": "t3",
      "files": ["inventory/plugins.py"],
      "depends_on": ["t2"],
      "summary": "Register the 'alert' formatter backed by report.format_alert"
    },
    {
      "id": "t4",
      "files": ["inventory/cli.py"],
      "depends_on": ["t2", "t3"],
      "summary": "Add --low-stock N to the report subcommand"
    }
  ]
}
```
