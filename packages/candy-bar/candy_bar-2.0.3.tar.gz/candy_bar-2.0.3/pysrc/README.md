# CandyBar

A Progress Bar inspired by Arch pacman with `ILoveCandy` option enabled.

![CandyBar](https://raw.githubusercontent.com/MacDumi/CandyBar/refs/heads/main/images/candybar.gif)

## Usage

Import the package and create the progress bar object:

```python
from candy_bar import CandyBar

cb = CandyBar(100, "Progress")
```

### Parameters

| Parameter      | Default        | Description                                             |
| ---            | ---            | ---                                                     |
| iterable       | `None`         | Iterable object                                         |
| total          | `None`         | Defines the value for 100% if not used with an iterable |
| message        | `None`         | Write some text at the beginning of the line            |
| messageWidth   | `message width`| Size (in chars) of the message (padded with spaces).    |
| width          | `console size` | Size (in chars) of the full progress bar.               |
| linePos        |   0            | Line position in case of nested progress bars.          |
| leftJustified  |   true         | Defines the justification of the message.               |
| disable        |   false        | When set, the progress bar will be disabled.            |

To update the position of the progress bar use the `update` method:

```python
total = 100

for i in range(total):
    # Your code goes here
    cb.update(i + 1)

# Use it as an iterable
for i in CandyBar(range(total), message="Progress"):
    # your code here
    # no need to call the update
```

The progress bar can be disabled:

```python
def function(verbose):
    ...
    cb.disable(not verbose)
    ...
```

The __total__ value, the __message__, and the __justification__ of the progress bar can be changed:

```python
cb.total = 150

cb.setMessage("Another message")
# optionally, provide the width of the message (will be padded with white spaces)
cb.setMessage("Another message", 32)

cb.setLeftJustified(False)
```

__Multiple progress bars__:

In case of nested progress bars, it is necessary to set the appropriate **linePos**.
The value should be 0 for the _lowest_ progress bar and incremented for higher ones.

```python
for i in CandyBar(range(100), message="Outer", linePos=1):
    for j in CandyBar(range(50), message="Inner", linePos=0):
        # your code here

# The linePos can be also updated
# cb = CandyBar(100, "Progress")
cb.linePos = 1
```


#### Like what I do?

Buy me coffee
<img src="https://web.getmonero.org/press-kit/symbols/monero-symbol-480.png" alt="Donate with monero" width="15"/> `85jJPcfLPZRUKm3Re6qHZsKBZskVS2tYMWFoY5sYXUSQJzqzqpuPFepXMtqTKCRfuhYXaiJ3zQVeRPDYJUfepVjnJDpApH5`
