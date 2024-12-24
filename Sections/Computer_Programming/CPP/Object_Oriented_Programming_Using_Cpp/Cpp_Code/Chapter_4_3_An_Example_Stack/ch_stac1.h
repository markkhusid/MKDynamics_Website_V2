// A simple implementation of type ch_stack

const int max_len = 1000;
enum { EMPTY = -1, FULL = max_len -1 };

struct ch_stack
{
    char s[max_len];
    int top;
};

// A standard set of ch_stack operations.

void reset(ch_stack * stk)
{
    stk -> top = EMPTY;
}

void push(ch_stack * stk, char c)
{
    stk -> s[++stk -> top] = c;  
}

char pop(ch_stack * stk)
{
    return (stk -> s[stk -> top--]);
}

char top(ch_stack * stk)
{
    return (stk -> s[stk -> top]);
}

bool empty(const ch_stack * stk)
{
    return (stk -> top == EMPTY); 
}

bool full(const ch_stack * stk)
{
    return (stk -> top == FULL);
}