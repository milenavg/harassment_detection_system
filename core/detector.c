#include "detector.h"
#include <string.h>

// TODO:
// - simple rule-based detection

int detect_toxicity(char *text) {
    if (strstr(text, "badword")) {
        return 1;
    }
    return 0;
}