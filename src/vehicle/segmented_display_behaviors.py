
def address_display(display, network_adapter):
    ipaddress = "    " + network_adapter[2][0]['addr']
    position = int(display.run_duration() / display.loop_delay()) % len(ipaddress)
    scrolling_ip_address = ipaddress[position:] + ipaddress[:position]
    display.set_text(scrolling_ip_address)
