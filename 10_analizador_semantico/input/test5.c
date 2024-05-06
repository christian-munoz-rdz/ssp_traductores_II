float distance(float x1, float y1, float x2, float y2) {
    float dx; 
    dx = x2 - x1;
    float dy;
    dy = y2 - y1;
    return sqrt(dx * dx + dy * dy);
}

void swap(int a, int b) {
    int temp;
    temp = a;
    a = b;
    b = temp;
}

int main() {
    float dist; 
    dist = distance(1.0, 1.0, 4.0, 5.0);
    int x , y;
    x = 10;
    y=20;
    swap(x, y);
    return 0;
}