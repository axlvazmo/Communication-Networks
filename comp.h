#define OP_SUM      0
#define OP_MEAN     1
#define OP_MIN      2
#define OP_MAX      3

#define TCP_PORT        5000

typedef struct{
    int opperation;
    double numbers[10];
}sBank_PROTOCOL;