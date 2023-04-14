
def load_file(filename):
    grids = list([])
    with open(filename, 'r') as file:
        str_f = file.read()
        lines = str_f.split('\n')

        grid = ""
        for line in lines:
            line = line.replace('.', '0').lower()
            if "," in line:
                grid += line.replace(',', '')
                grids.append(grid)
                grid = ""
                # break
            else:
                grid += line

    return grids


def save_file(output_filename, grids):
    with open(output_filename, 'w') as fp:
        for grid in grids:
            # write each grid on a new line
            fp.write("%s\n" % grid)
    return True


def main():
    formatted_grids = load_file('grilles36.txt')
    print(len(formatted_grids))
    file_saved = save_file('grille_36_formatted.txt', formatted_grids)
    if file_saved:
        print("File saved successfully!")
    else:
        print("Oops, something went wrong while trying to output data in file. ")


if __name__ == "__main__":
    main()
