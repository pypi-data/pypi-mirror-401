#include "hello_c.h"

#ifdef __cplusplus
extern "C" {
#endif

int add_ints(int a, int b) {
    return a + b;
}

#ifdef __cplusplus
}
#endif
