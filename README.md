# Foundation Library
The Foundation Python Library is your gateway to effortless interaction with the Foundation API. Designed with simplicity and efficiency in mind, this library abstracts away the complexity of direct API calls, providing a clean and intuitive interface for developers. 

## Installation

```
pip install teleology-foundation
```

or install from source:

```
python setup.py install
```

## Requirements
- requests >= 2.32.2
- websocket-client >= 1.8.0

## Usage Example:
```python
from foundation import Foundation

def subscriber(event: str, data): 
  print(f"Received event '{event}': {data}")

def main():
  client = Foundation(url='https://foundation-api.teleology.io', apiKey='<your-api-key>', uid='<user-unique-id>')

  client.subscribe(subscriber)


  print("getEnvironment", client.getEnvironment())
  print("getConfiguration", client.getConfiguration())
  print("getVariable", client.getVariable(name="variable_name", uid='<user-id-override>', fallback=20))



if __name__ == "__main__":
  main()
```