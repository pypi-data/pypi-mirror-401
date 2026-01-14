
import json, sys, argparse
from xml.etree.ElementTree import Element, tostring

def dict_to_xml(tag, d):
    elem = Element(tag)
    for k, v in d.items():
        child = Element(str(k))
        child.text = str(v)
        elem.append(child)
    return elem

def main():
    p = argparse.ArgumentParser(description="Convert JSON to XML")
    p.add_argument("input", help="Input JSON file")
    args = p.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    root = dict_to_xml("root", data if isinstance(data, dict) else {"item": data})
    sys.stdout.write(tostring(root, encoding="unicode"))

if __name__ == "__main__":
    main()
