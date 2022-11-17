import csv


def unique_list(start_list: list) -> list:
    end_list = []
    for el in start_list:
        if el not in end_list:
            end_list.append(el)
    return end_list


def write_to_csv_file(elements: list):
    file = open('frenchpress_more_data_output.csv', 'a', newline='')
    writer = csv.writer(file, delimiter=';')
    writer.writerows(elements)
