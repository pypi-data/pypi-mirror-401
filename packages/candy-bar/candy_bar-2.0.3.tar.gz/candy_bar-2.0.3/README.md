[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMacDumi%2FCandyBar.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FMacDumi%2FCandyBar?ref=badge_shield)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/candy-bar.svg)](https://pypi.org/project/candy-bar/)
[![Downloads](https://pepy.tech/badge/candy-bar)](https://pepy.tech/project/candy-bar)
[![Downloads/Month](https://pepy.tech/badge/candy-bar/month)](https://pepy.tech/project/candy-bar)

# CandyBar

A Progress Bar inspired by Arch pacman with `ILoveCandy` option enabled.

![CandyBar](https://raw.githubusercontent.com/MacDumi/CandyBar/refs/heads/main/images/candybar.gif)

## Instalation

<details open>
<summary><span style="font-size: 1.5em; font-weight:bold;">Python</span></summary>

#### Manual instalation

Clone the repository, build, and install the package:

```bash
git clone https://github.com/MacDumi/CandyBar.git
cd CandyBar
pip install .
```
**Note:** This requires a C++ compiler.

#### Install from PyPi

```bash
pip install candy-bar
```

</details>

<details>
<summary><span style="font-size: 1.5em; font-weight:bold;">C++</span></summary>


Clone the repository and either install the library or build against it:

```bash
git clone https://github.com/MacDumi/CandyBar.git
cd CandyBar
make && sudo make install
```

</details>

## Usage

<details open>
<summary><span style="font-size: 1.5em; font-weight:bold;">Python</span></summary>

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

</details>

<details>
<summary><span style="font-size: 1.5em; font-weight:bold;">C++</span></summary>

Include the header file and create the progress bar object:

```C++
#include "candybar.h"

...

CandyBar cb(100, "Progress");
```

### Parameters

| Parameter      | Default        | Description                                             |
| ---            | ---            | ---                                                     |
| total          | --             | Defines the value corresponding to 100%                 |
| message        | `None`         | Write some text at the beginning of the line            |
| messageWidth   | `message width`| Size (in chars) of the message (padded with spaces).    |
| width          | `console size` | Size (in chars) of the full progress bar.               |
| linePos        |   0            | Line position in case of nested progress bars.          |
| leftJustified  |   true         | Defines the justification of the message.               |
| disable        |   false        | When set, the progress bar will be disabled.            |

To update the position of the progress bar use the `update` method:

```C++
constexpr uint32_t total{100};

for (auto i{0}; i < total; ++i)
{
    // Your code goes here
    cb.update(i);
}
```
The progress bar can be disabled:

```C++
void function(bool verbose)
{
    ...
    cb.disable(!verbose);
    ...
}
```

The __total__ value, the __message__, and the __justification__ of the progress bar can be changed:

```C++
cb.setTotal(150);

cb.setMessage("Another message");
// optionally, provide the width of the message (will be padded with white spaces)
cb.setMessage("Another message", 32);

cb.setLeftJustified(false);
```

__Multiple progress bars__:

In case of nested progress bars, it is necessary to set the appropriate **linePos**.
The value should be 0 for the _lowest_ progress bar and incremented for higher ones.

```C++
cb_top.setLinePos(1);
cb_bottom.setLinePos(0);

for (auto i{0}; i < cb_top.getTotal(); ++i)
{
    for (auto j{0}; j < cb_bottom.getTotal(); ++j)
    {
        // your code here
        cb_bottom.update(j);
    }
    cb_top.update(i);
}

// The linePos can be also updated
// CandyBar cb(100, "Progress");
cb.setLinePos(1);
```
</details>

#### Like what I do?

Buy me coffee
<img src="https://web.getmonero.org/press-kit/symbols/monero-symbol-480.png" alt="Donate with monero" width="15"/> `85jJPcfLPZRUKm3Re6qHZsKBZskVS2tYMWFoY5sYXUSQJzqzqpuPFepXMtqTKCRfuhYXaiJ3zQVeRPDYJUfepVjnJDpApH5`
