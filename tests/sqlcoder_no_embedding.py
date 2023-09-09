from SQLCoder import SQLCoder
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='sqlcoder: generate SQL using the power of LLMs.')

    parser.add_argument("-n", "--model-name", type=str,
                        default="defog/sqlcoder", help="Name of the model to use")

    parser.add_argument("-s", "--select", type=str,
                        default="example", help="Selection of prompt")

    parser.add_argument("-E", "--use-embedding", action='store_true',
                        help='Use this flag to enable embedding for context generation.')

    return parser.parse_args()


def main():
    args = parse_arguments()

    sqlcoder_no_embedding = SQLCoder(
        model_name=args.model_name, use_embedding=False)

    print(sqlcoder_no_embedding("给我一句查询数据库中所有表结构的语句"))


if __name__ == "__main__":
    main()
