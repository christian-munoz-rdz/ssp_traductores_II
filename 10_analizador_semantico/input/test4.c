int max(int a, int b) { 
    if (a > b) { 
        return a; 
    } else { 
        return b; 
    } 
}
int factorial(int n) { 
    if (n == 0) { 
        return 1; 
    } else { 
        return n * factorial(n - 1); 
    } 
}
int main() { 
    int num1, num2;
    num1 = 5; 
    num2 = 10; 
    int m;
    m = max(num1, num2); 
    int f; 
    f = factorial(m); 
    return f; 
}
