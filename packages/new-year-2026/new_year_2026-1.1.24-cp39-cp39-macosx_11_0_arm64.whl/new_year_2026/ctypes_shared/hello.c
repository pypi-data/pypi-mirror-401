#include <stdio.h>

#if defined(_WIN32)
#define API __declspec(dllexport)
#else
#define API
#endif

API int add_ints(int a, int b) {
    return a + b;
}

API const char *hello(void) {
    return "hello from C";
}
