
def parsePropBack(prop):
    types = ["fileStorage", "metadata"]

    data = [
        {"portType": typ, "value": True}
        for typ in types
        if typ in prop["type"]
    ]

    customProp = [{"key": key, "value": value}
                  for key, value in prop.get("customProperties", {}).items()]

    data.append({"portType": "customProperties", "value": customProp})
    print(data)

    return data


def parsePortBack(port):
    return {
        "port": port["port"],
        "properties": parsePropBack(port["properties"])
    }


def parseResearchBack(response):
    data = {
        "portIn": [parsePortBack(port) for port in response["portIn"]],
        "portOut": [parsePortBack(port) for port in response["portOut"]]
    }
    response.update(data)
    return response


def parseCustomProp(customProp):
    return {val["key"]: val["value"] for val in customProp}


def parseProp(prop):
    propList = {"type": []}
    for val in prop:
        if val["portType"] == "customProperties":
            propList["customProperties"] = parseCustomProp(val["value"])
        else:
            propList["type"].append(val["portType"])
    return propList


def parsePort(port):
    return {
        "port": port["port"],
        "properties": parseProp(port["properties"])
    }


def parseResearch(response):

    data = {
        "portIn": [parsePort(port) for port in response["portIn"]],
        "portOut": [parsePort(port) for port in response["portOut"]]
    }
    response.update(data)
    return response


def parseAllResearch(response):
    return [parseResearch(research) for research in response]


def parseAllResearchBack(response):
    return [parseResearchBack(research) for research in response]
