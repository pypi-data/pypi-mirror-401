from typing import List, Optional, TypeVar

T = TypeVar("T")


def swap_str(value: str, old: str, new: str) -> str:
    """
    Walk in the current string using n_gram and swaps the old by the new.
    Example:
          ```
          value = "200.000,99"
          old = ","
          new = "."
          result = "200,000.99"

          value "abcdecdf"
          old = "bc"
          new = "cd"
          result = "acddebcf"
          ```
     Please note that in the last example there is the sequence "bcd"
     and the algorithm will perform the replacement on the first match.
    """
    if old == new:
        return value

    step = len(old)
    new_str = ""
    for element in n_gram(value, step):
        if element == old:
            new_str += new
        elif element == new:
            new_str += old
        else:
            new_str += str(element)
    return new_str


def n_gram(value: List[T] | str, size: int) -> List[List[T]] | List[str]:
    """
    It is similar to a batch structure, but slightly different.
    Examples are the best!
    Output size will always be size.
    Example:
      ```
      value = [1, 2, 3]
      size = 2
      result = [[1, 2], [2, 3]]

      value = 'hey, how are you'
      size = 2
      result = ['he', 'ey', 'y,', ', ', ' h', 'ho', 'ow', 'w ',
      ' a', 'ar', 're', 'e ', ' y', 'yo', 'ou']
      ```
    """
    if len(value) <= size:
        return [str(value)]

    combinations = []
    for idx in range(0, len(value) - (size - 1)):
        current_value = value[idx]
        next_value = value[idx + 1]
        combinations.append([current_value, next_value])
    return combinations


def batch(value: List[T] | str, size: int) -> List[List[T]] | List[str]:
    """
    An alternative to passing a step value directly to range,
    since range doesn't include the last value.
    Output size will always be [size | size - 1]
    Example:
      ```
      value = [1, 2, 3]
      size = 2
      result = [[1, 2], [3]]

      value = 'hey, how are you'
      size = 2
      result = ['he', 'y,', ' h', 'ow', 'ar', 'e ', 'yo', 'u']
      ```
    """
    if len(value) < size:
        raise ValueError(
            f"Value {value} too short to batch in steps with size {size}.")
    batches, current_batch, elements_added = [], [], 0

    for element in value:
        if elements_added >= size:
            batches.append(current_batch)
            elements_added, current_batch = 1, []
        current_batch.append(element)
        elements_added += 1
    return batches


def parse_float_or_none(value: Optional[str | int | float]) -> Optional[float]:
    if value is None:
        return value
    try:
        return float(value)
    except Exception:
        try:
            return float(swap_str(str(value), ",", ".").replace(",", ""))
        except Exception:
            return None
