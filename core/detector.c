#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_TEXT 2000

// CAPS RATIO
float get_caps_ratio(const char* text) {

    int len = strlen(text);
    if (len == 0) return 0;

    int caps = 0;

    for (int i = 0; i < len; i++) {
        if (isupper(text[i])) {
            caps++;
        }
    }

    return (float)caps / len;
}

// REPETITION SCORE (character-level)
float get_repetition_score(const char* text) {

    int len = strlen(text);
    if (len < 2) return 0;

    int repeats = 0;

    for (int i = 1; i < len; i++) {
        if (text[i] == text[i - 1]) {
            repeats++;
        }
    }

    return (float)repeats / len;
}

// MAIN FUNCTION (EXPORTED TO PYTHON)
char* analyze_text(const char* text) {

    static char result[256];

    float caps = get_caps_ratio(text);
    float rep = get_repetition_score(text);

    snprintf(
        result,
        sizeof(result),
        "{\"caps_ratio\": %.3f, \"repetition_score\": %.3f}",
        caps,
        rep
    );

    return result;
}