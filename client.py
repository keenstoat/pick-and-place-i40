#!/usr/bin/env python3

import asyncio
from asyncua import Client, ua
from re import sub


async def main(url, ns_url):

    print(f"Connecting to OPCUA server at {url} ...")
    async with Client(url=url) as client:

        ns = 2 # await client.get_namespace_index(ns_url)

        def path_fix(path:str):
            # return path
            return "/".join([f"{ns}:{sub(r'\d:', '', seg)}" for seg in path.split("/")])

        submodel_node = await client.nodes.objects.get_child(path_fix("2:AASEnvironment/2:FunctionsSubModel"))

        processed_item_count_node = await submodel_node.get_child(path_fix("2:processedItemCount/2:Value"))
        val = await processed_item_count_node.read_value()
        print("BEFORE processedItemCount: ", val)
        await processed_item_count_node.write_value(val + 2)

        val = await processed_item_count_node.read_value()
        print("AFTER processedItemCount: ", val)



        pickup_node = await submodel_node.get_child("2:pickup")
        response = await pickup_node.call_method("3:pickup", ua.Float(3.4), ua.Float(09.3))
        print("RESP: ", response)


if __name__ == "__main__":

    url = "opc.tcp://localhost:4840/"
    ns = "http://idtt/sorting_module/"
    asyncio.run(main(url, ns))