# Pydantic Snowflake ID

A Pydantic custom type for validating and serializing Snowflake IDs.

## Features
- Custom Pydantic type `SnowflakeId` for Snowflake ID validation.
- `SnowflakeGenerator` for generating unique Snowflake IDs.
- Supports custom epochs, worker IDs, and process IDs.
- Supports serialization and deserialization of pydantic models with Snowflake IDs.

## Installation
You can install the package via pip:

```bash
pip install -U pydantic-snowflakes
```

## Usage
```python
from pydantic import BaseModel
from pydantic_snowflake import SnowflakeId, SnowflakeGenerator

from datetime import datetime

custom_epoch = datetime(2020, 1, 1)

class User(BaseModel):
    id: SnowflakeId
    name: str

# Generating a Snowflake ID
generator = SnowflakeGenerator(
    epoch=custom_epoch,
    worker_id=0,
    process_id=0
)

new_id = generator.next()
user = User(id=new_id, name="Alice")
print(user)

# Generating multiple Snowflake IDs
for _id in [generator.next() for _ in range(5)]:
    user = User(id=_id, name="Bob")
    print(user)
```

## License
```
MIT License

Copyright (c) 2025-2026, Chih-Hao Chuang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
