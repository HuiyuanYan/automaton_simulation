import test_DFA
import test_NFA


def test_all():
    """test all the test files
    """
    print('Executing tests...\n')

    print('testing test_DFA...')
    test_DFA.test_all()
    print('test result: \033[32mpass\033[0m\n')

    print('testing test_NFA...')
    test_NFA.test_all()
    print('test result: \033[32mpass\033[0m\n')

    print('All tests passed.')


if __name__ == "__main__":
    test_all()
