import DFA_test
import NFA_test


def test_all():
    """test all the test files
    """
    print('Executing tests...\n')

    print('testing DFA_test...')
    DFA_test.test_all()
    print('test result: \033[32mpass\033[0m\n')

    print('testing NFA_test...')
    NFA_test.test_all()
    print('test result: \033[32mpass\033[0m\n')

    print('All tests passed.')


if __name__ == "__main__":
    test_all()
