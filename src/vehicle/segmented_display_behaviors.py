
def address_display(display, network_adapter):
    ipaddress = "    "
    if len(network_adapter)>2 and len(network_adapter[2]) > 0 and network_adapter[2][0].__contains__('addr'):
        ipaddress += network_adapter[2][0]['addr']
    else:
        ipaddress += "127.0.0.1"

    position = int(display.run_duration() / display.loop_delay()) % len(ipaddress)
    scrolling_ip_address = ipaddress[position:] + ipaddress[:position]
    display.set_text(scrolling_ip_address)
