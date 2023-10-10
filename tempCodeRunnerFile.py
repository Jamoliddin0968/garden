import struct


def calculate_floating_point_value(bit_representation, data_type):
    """Calculates the value of a 64-bit floating-point variable.

    Args:
      bit_representation: A 64-bit integer representing the bit representation of
        the variable.
      data_type: A string representing the data type of the variable.

    Returns:
      The value of the variable as a floating-point number.
    """

    sign_bit = (bit_representation >> 63) & 1
    exponent = (bit_representation >> 52) & 1023
    mantissa = (bit_representation >> 23) & 1023

    # Calculate the bias.
    bias = 1023 if data_type == 'float64' else 127

    # Calculate the value of the variable.
    value = (-1)**sign_bit * 2**(exponent - bias) * (1 + mantissa / 1024)

    return value

# Example usage:


bit_representation = 4608871268660281344
data_type = 'float64'

value = calculate_floating_point_value(bit_representation, data_type)

print(value)
