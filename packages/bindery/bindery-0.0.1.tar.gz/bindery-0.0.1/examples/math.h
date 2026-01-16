#ifndef MATH_H
#define MATH_H

namespace math {

class Calculator {
public:
    Calculator() {}
    
    int add(int a, int b) {
        return a + b;
    }
    
    int subtract(int a, int b) {
        return a - b;
    }
};

} // namespace math

#endif // MATH_H
