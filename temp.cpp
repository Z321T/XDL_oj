#include <iostream>
#include <cmath>

bool isPrime(int num) {
    if (num <= 1) {
        return false;
    }
    if (num <= 3) {
        return true;
    }

    if (num % 2 == 0 || num % 3 == 0) {
        return false;
    }

    for (int i = 5; i * i <= num; i += 6) {
        if (num % i == 0 || num % (i + 2) == 0) {
            return false;
        }
    }

    return true;
}

int main() {
    std::cout << "Prime numbers between 1 and 20 are: ";

    for (int num = 1; num <= 20; ++num) {
        if (isPrime(num)) {
            std::cout << num << " ";
        }
    }

    std::cout << std::endl;
    return 0;
}
