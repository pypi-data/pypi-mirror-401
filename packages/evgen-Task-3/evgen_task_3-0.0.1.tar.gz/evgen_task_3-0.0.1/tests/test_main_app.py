import pytest
from package.src.main_app import get_unique_count


def test_get_unique_count(mocker):
    mock_file = mocker.patch('package.src.main_app.open', mocker.mock_open(read_data='test'))

    result = get_unique_count('fake_patch.txt')

    assert result == 2
    mock_file.assert_called_with('fake_patch.txt', 'r', encoding='utf-8')

def test_invalid_input():
    with pytest.raises(TypeError):
        # Перевірка чи не падає функція якщо передати число
        assert get_unique_count(123)

@pytest.mark.parametrize("input_str, expected_result", [
    ("abcabctj", 2),
    ("abcdef", 6),
    ("aaaaaa", 0),
    ("", 0),
    ("aabbcde", 3)
])
def test_multiple_string(input_str, expected_result):
    assert get_unique_count(input_str) == expected_result