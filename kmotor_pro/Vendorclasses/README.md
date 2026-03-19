# Vendorclasses

One JSON file per vendor/manufacturing class.

Each parameter uses the same normalized schema:

```json
{
  "min": null,
  "rec": null,
  "max": null
}
```

Intended later for:
- preset loading
- min/max validation
- warnings when current values leave the selected vendor class
- contextual parameter help in the GUI

Current state:
- placeholder templates only
- vendor values still need to be collected and filled in
