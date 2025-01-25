import re


def __replace_multiple_whitespace(input_string):
    # Use regular expression to replace multiple consecutive whitespaces with a single whitespace
    output_string = re.sub(r'[\n]+', ' \n ', input_string)
    output_string = re.sub(r'[\t]+', ' ', output_string)
    output_string = re.sub(r'[\r]+', '', output_string)
    output_string = re.sub(r'[ ]+', ' ', output_string)

    # Remove leading and trailing whitespaces around each newline
    output_string = re.sub(r'(\n)[\t\r ]*|[\t\r ]*(\n)', r'\1', output_string)

    return output_string

def clear_formatting(input_string):
    return __replace_multiple_whitespace(input_string)

if __name__ == '__main__':
    # Example usage
    # input_text = "Hello\n\n\n World! \n\n\n\n\t   How\tare\tyou? \n"
    input_text = '''for index, row in df.iterrows():


        project = row['project']
        sub_project = row['sub_project']

        if project == 'Previous':
            continue

        new_df.loc[len(new_df)] = row'''
    print("input_text:", input_text)
    output_text = __replace_multiple_whitespace(input_text)
    print(output_text)
