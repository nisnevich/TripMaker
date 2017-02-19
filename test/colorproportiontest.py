def rgb_to_hex(rgb):
    ''' [255,255,255] -> "#FFFFFF" '''
    rgb = [int(x) for x in rgb]
    return "#" + "".join(["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in rgb])


def get_proportion_color(min_price, max_price, current_price):
    blue_component = 0

    max_price_normalized = max_price - min_price
    current_price_normalized = current_price - min_price
    half_price = max_price_normalized / 2

    if max_price_normalized == 0:
        red_component = 0
        green_component = 255
    elif current_price - min_price < half_price:
        # red is increasing, green is maximal
        red_component = round(current_price_normalized * 255 / half_price)
        green_component = 255
    else:
        # red is maximal, green is decreasing
        current_price_normalized -= half_price
        red_component = 255
        green_component = 255 - round(current_price_normalized * 255 / half_price)

    return [red_component, green_component, blue_component]

res = get_proportion_color(1276, 5694, 5694)
print(res)
