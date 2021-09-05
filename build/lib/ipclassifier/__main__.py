from ipclassifier.runners import classify_ip, train_runner
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(description="English Iambic Pentameter Period Classifier")
    parser.add_argument("-f", dest="filename", required=True,
                        help="Input .txt file.  Assumes the file is in user_input_poems/. \
                              File should contain newline-separated iambic pentameter. \
                              Performance is best with 100 or more lines. "
                       )
    parser.add_argument('--train', dest="train", action="store_true", help='Set to train a new model.')    
    args = parser.parse_args()
    if args.train:
        print('training...')
        train_runner()
    else:
        classify_ip(f"{args.filename}")
