#!/usr/bin/env python3

import asyncio
from asyncua import Server, ua
from yaml import safe_load

async def main():
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://localhost:4841")

    # set up our own namespace, not really necessary but should as spec
    uri = "http://assetopcuaapi"
    idx = await server.register_namespace(uri)
    objects = server.nodes.objects
    asset = await objects.add_object(idx, "asset")

    with open("model.yaml") as model_file:
        model = safe_load(model_file)

    for obj in model:
        if obj["objectType"] == "variable":
            value = getattr(ua, obj["valueType"])(obj["value"])
            myvar = await asset.add_variable(idx, obj["name"], value)
            obj["ua_variable_node"] = myvar
            if obj.get("writable"):
                await myvar.set_writable()
        
        elif obj["objectType"] == "method":
            await asset.add_method(
                ua.NodeId(obj["name"], idx),
                ua.QualifiedName(obj["name"], idx),
                getattr(__import__("uamethods"), obj["function"]),
                [getattr(ua.VariantType, variant) for variant in obj["inputVariables"]],
                [getattr(ua.VariantType, variant) for variant in obj["outputVariables"]],
            )

    async with server:
        while True:
            for obj in model:
                if obj["objectType"] == "variable":
                    value = getattr(__import__("uamethods"), obj["function"])()
                    value = getattr(ua, obj["valueType"])(value)
                    await obj["ua_variable_node"].write_value(value)
            
            await asyncio.sleep(0.1)



if __name__ == "__main__":
    asyncio.run(main(), debug=True)