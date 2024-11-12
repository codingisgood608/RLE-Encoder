import console_gfx


def display_menu():
    print("\nRLE Menu\n"
          "--------")
    print("0. Exit")
    print("1. Load File")
    print("2. Load Test Image")
    print("3. Read RLE String")
    print("4. Read RLE Hex String")
    print("5. Read Data Hex String")
    print("6. Display Image")
    print("7. Display RLE String")
    print("8. Display Hex RLE Data")
    print("9. Display Hex Flat Data")
    print()


def to_hex_string(data):
    return ''.join(f'{x:x}' for x in data)


def count_runs(flat_data):
    if not flat_data:
        return 0
    runs = 0
    current_run_value = flat_data[0]
    current_run_length = 1
    for pixel in flat_data[1:]:
        if pixel == current_run_value:
            current_run_length += 1
            if current_run_length == 15:
                runs += 1
                current_run_length = 0
        else:
            if current_run_length > 0:
                runs += 1
            current_run_value = pixel
            current_run_length = 1
    if current_run_length > 0:
        runs += 1
    return runs


def encode_rle(flat_data):
    if not flat_data:
        return []
    rle = []
    current_run_value = flat_data[0]
    current_run_length = 1

    for pixel in flat_data[1:]:
        if pixel == current_run_value:
            current_run_length += 1
            while current_run_length > 15:
                rle.append(15)
                rle.append(current_run_value)
                current_run_length -= 15
        else:
            if current_run_length > 0:
                rle.append(current_run_length)
                rle.append(current_run_value)
            current_run_value = pixel
            current_run_length = 1

    if current_run_length > 0:
        rle.append(current_run_length)
        rle.append(current_run_value)

    return rle


def get_decoded_length(rle_data):
    return sum(rle_data[i] for i in range(0, len(rle_data), 2))


def decode_rle(rle_data):
    flat_data = []
    for i in range(0, len(rle_data), 2):
        run_length = rle_data[i]
        run_value = rle_data[i + 1]
        flat_data.extend([run_value] * run_length)
    return flat_data


def string_to_data(data_string):
    return [int(char, 16) for char in data_string]


def to_rle_string(rle_data):
    return ':'.join(f"{rle_data[i]}{rle_data[i + 1]:x}" for i in range(0, len(rle_data), 2))


def string_to_rle(rle_string):
    runs = rle_string.split(':')
    rle_data = []
    for run in runs:
        length = int(run[:-1])
        value = int(run[-1], 16)
        rle_data.extend([length, value])
    return rle_data


def main():
    print("Welcome to the RLE image encoder!\n")
    print("Displaying Spectrum Image:")
    console_gfx.display_image(console_gfx.test_rainbow)
    image_data = []

    while True:
        display_menu()
        option = int(input("Select a Menu Option: "))
        if option == 0:
            break
        elif option == 1:
            file_name = input("Enter the name of the file name: ")
            image_data = console_gfx.load_file(file_name)
            print()
        elif option == 2:
            image_data = console_gfx.test_image
            print("Test image data loaded.\n")
        elif option == 3:
            rle_string = input("Enter an RLE string to be decoded: ")
            image_data = decode_rle(string_to_rle(rle_string))
            print()
        elif option == 4:
            hex_string = input("Enter the hex string holding RLE data: ")
            image_data = decode_rle(string_to_data(hex_string))
            print()
        elif option == 5:
            flat_hex = input("Enter the hex string holding flat data: ")
            image_data = string_to_data(flat_hex)
            print()
        elif option == 6:
            print("Displaying image...")
            console_gfx.display_image(image_data)
            print()
        elif option == 7:
            print("RLE representation:", to_rle_string(encode_rle(image_data)))
            print()
        elif option == 8:
            print("RLE hex values:", to_hex_string(encode_rle(image_data)))
            print()
        elif option == 9:
            print("Flat hex values:", to_hex_string(image_data))
            print()


if __name__ == "__main__":
    main()/