**Example configuration.yaml:**

```yaml
sensor:
  platform: wienerlinien
  apikey: 2190400
  firstnext: first
  stops:
    - '4429'
    - '3230'
```

**Configuration variables:**

key | description
:--- | :---
**platform (Required)** | The platform name.
**apikey (Required)** | Your API key from wien.gv.at.
**stops (Required)** | RBL stop ID's
**firstnext (Optional)** | `first` or `next` departure.

![Sample overview](https://raw.githubusercontent.com/custom-components/wienerlinien/master/overview.png)

