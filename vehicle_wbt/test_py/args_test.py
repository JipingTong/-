import argparse
def arg_test():
    parser = argparse.ArgumentParser()
    parser.add_argument('--foo', help='foo help')
    args = parser.parse_args()
    print(args.foo)

def list_test():
    list1= ['a', 'b', 'c']
    a, b, c = list1
    print(a, b,c )

if __name__ == "__main__":
    # arg_test()
    list_test()