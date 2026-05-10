#include <stdio.h>
#include "detector.h"

// TODO:
// - test detection engine

int main() {
    char text[] = "hello world";
    printf("Result: %d\n", detect_toxicity(text));
    return 0;
}