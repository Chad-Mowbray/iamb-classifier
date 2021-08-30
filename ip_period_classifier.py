from runners import classify_ip


if __name__ == "__main__":
    from argparse import ArgumentParser


    parser = ArgumentParser(description="English Iambic Pentameter Period Classifier")
    parser.add_argument("-f", dest="filename", required=True,
                        help="Input .txt file.  Assumes the file is in user_input_poems/. \
                              File should contain newline-separated iambic pentameter. \
                              Performance is best with 100 or more lines. "
                       )
    args = parser.parse_args()
    classify_ip(f"user_input_poems/{args.filename}")
