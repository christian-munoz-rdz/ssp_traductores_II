int var1, var2, var3, var4, var5; 

float calcularPromedio(int a, int b, int c, int d, int e) { 
    int suma;
    suma = a + b + c + d + e; 
    float promedio;
    promedio = suma / 5.0; 
    return promedio; 
}

float calcularVarianza(int a, int b, int c, int d, int e, float promedio) { 
    float varianza; 
    varianza= ((a - promedio) * (a - promedio) + (b - promedio) * (b - promedio) + (c - promedio) * (c - promedio) + (d - promedio) * (d - promedio) + (e - promedio) * (e - promedio)) / 5.0; 
    return varianza; 
}
