
def address_display(display, network_adapter):
    if len(network_adapter)>2 and len(network_adapter[2]) > 0 and network_adapter[2][0].__contains__('addr'):
        ipaddress = network_adapter[2][0]['addr']
    else:
        ipaddress = "127.0.0.1"

    #group decimals with preceeding character
    digitDecimalPairs = [(' ',''),(' ',''),(' ',''),(' ','')]
    while len(ipaddress) > 0:
        digit = ipaddress[0]
        ipaddress = ipaddress[1:]
        decimal = ''
        if len(ipaddress) > 0 and ipaddress[0] == '.':
            decimal = ipaddress[0]
            ipaddress = ipaddress[1:]

        digitDecimalPairs.append((digit, decimal))

    position = int(display.run_duration() / display.loop_delay()) % len(digitDecimalPairs)

    textToDisplay = ''
    for dp in (digitDecimalPairs[position:] + digitDecimalPairs[:position])[:4]:
        textToDisplay += dp[0]
        textToDisplay += dp[1]

    display.set_text(textToDisplay)
