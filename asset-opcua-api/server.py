#!/usr/bin/env python3

import asyncio
import logging
from re import sub
from asyncua import Server, ua
from asyncua.common.node import Node as UaNode
import uamethods as uam
from sys import exit

class AssetServer:

    def __init__(self, namespace, server_name, server_endpoint, model_xml_filepath):

        self.server = Server()
        self.server.set_server_name(server_name)
        self.server.set_endpoint(server_endpoint)
        self.namespace = namespace
        self.model_xml_filepath = model_xml_filepath

    def value_to_variant(self, value, variant_type:ua.VariantType):
        try:
            variant_type = str(variant_type).split(".")[-1]
            return True, getattr(ua, variant_type)(value)
        except:
            return False, value
    
    async def start(self):

        await self.server.init()
        await self.server.import_xml(self.model_xml_filepath)

        objects = self.server.nodes.objects
        ns = await self.server.get_namespace_index(self.namespace)

        def path_fix(path:str):
            return "/".join([f"{ns}:{sub(r'\d:', '', seg)}" for seg in path.split("/")])

        ua_model_method_mapping = [
            {
                "ua_method_node": "asset/pickup", 
                "function": uam.pickup
            }
        ]
        
        for mapping in ua_model_method_mapping:
            print(f"- Mapping UA method '{mapping["ua_method_node"]}'")
            self.server.link_method(await objects.get_child(path_fix(mapping["ua_method_node"])), mapping["function"])

        ua_model_variable_mapping = [ 
            {
                "ua_variable_node": await objects.get_child(path_fix("asset/processedItemCount")),
                "value": uam.get_processed_item_count
            },
        ]

        print()
        async with self.server:
            while True:
                await asyncio.sleep(0.1)

                for mapping in ua_model_variable_mapping:
                    node:UaNode = mapping["ua_variable_node"]
                    value = mapping["value"]
                    value = value() if callable(value) else value
                    variant_type = await node.read_data_type_as_variant_type()
                    _, value = self.value_to_variant(value, variant_type)
                    await node.write_value(value)


if __name__ == "__main__":
    ip_addr = "127.0.0.1"
    print("IP Address: ", ip_addr)
    print()
    opcua_server = AssetServer(
        "http://asset-api/",
        "Asset API OPCUA Server",
        f"opc.tcp://{ip_addr}:4841",
        "asset-model/asset-model.xml",
    )
    try:
        asyncio.run(opcua_server.start())
    except KeyboardInterrupt:
        exit(0)
    
